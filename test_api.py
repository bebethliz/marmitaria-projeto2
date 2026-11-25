"""Testes da API: CRUD das duas entidades e todas as regras de validação."""

import os
import tempfile
import unittest

from app import create_app


class BaseApiTest(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        caminho = os.path.join(self.pasta.name, "teste.db")
        self.cliente = create_app(caminho, semear=False).test_client()

    def tearDown(self):
        self.pasta.cleanup()

    def criar_categoria(self, nome="Marmitas", descricao=""):
        resposta = self.cliente.post("/api/categorias", json={"nome": nome, "descricao": descricao})
        self.assertEqual(resposta.status_code, 201, resposta.get_json())
        return resposta.get_json()

    def criar_prato(self, categoria_id, **extras):
        dados = {"nome": "Feijoada", "preco": 24.9}
        dados.update(extras)
        return self.cliente.post(f"/api/categorias/{categoria_id}/pratos", json=dados)


class CategoriaTest(BaseApiTest):
    def test_crud_completo(self):
        criada = self.criar_categoria("Bebidas", "Sucos e refrigerantes")
        self.assertEqual(criada["total_pratos"], 0)

        lista = self.cliente.get("/api/categorias").get_json()
        self.assertEqual([c["nome"] for c in lista], ["Bebidas"])

        resposta = self.cliente.put(f"/api/categorias/{criada['id']}", json={"nome": "Bebidas geladas"})
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json()["nome"], "Bebidas geladas")

        self.assertEqual(self.cliente.delete(f"/api/categorias/{criada['id']}").status_code, 204)
        self.assertEqual(self.cliente.get(f"/api/categorias/{criada['id']}").status_code, 404)

    def test_nome_obrigatorio(self):
        for nome in ["", "   ", None]:
            resposta = self.cliente.post("/api/categorias", json={"nome": nome})
            self.assertEqual(resposta.status_code, 400)
            self.assertIn("nome", resposta.get_json()["campos"])

    def test_nome_repetido_ignora_maiusculas_e_espacos(self):
        self.criar_categoria("Sobremesas")
        resposta = self.cliente.post("/api/categorias", json={"nome": "  sobremesas "})
        self.assertEqual(resposta.status_code, 409)
        self.assertIn("nome", resposta.get_json()["campos"])

    def test_atualizar_mantendo_o_proprio_nome_e_permitido(self):
        categoria = self.criar_categoria("Fit")
        resposta = self.cliente.put(
            f"/api/categorias/{categoria['id']}", json={"nome": "Fit", "descricao": "Leves"}
        )
        self.assertEqual(resposta.status_code, 200)

    def test_atualizar_para_nome_de_outra_categoria_e_bloqueado(self):
        self.criar_categoria("Fit")
        outra = self.criar_categoria("Bebidas")
        resposta = self.cliente.put(f"/api/categorias/{outra['id']}", json={"nome": "FIT"})
        self.assertEqual(resposta.status_code, 409)

    def test_nao_exclui_categoria_com_pratos(self):
        categoria = self.criar_categoria()
        prato = self.criar_prato(categoria["id"]).get_json()

        resposta = self.cliente.delete(f"/api/categorias/{categoria['id']}")
        self.assertEqual(resposta.status_code, 409)
        self.assertIn("1 prato", resposta.get_json()["erro"])

        self.cliente.delete(f"/api/pratos/{prato['id']}")
        self.assertEqual(self.cliente.delete(f"/api/categorias/{categoria['id']}").status_code, 204)

    def test_contagem_de_pratos_na_listagem(self):
        categoria = self.criar_categoria()
        self.criar_prato(categoria["id"])
        self.criar_prato(categoria["id"], nome="Strogonoff")
        lista = self.cliente.get("/api/categorias").get_json()
        self.assertEqual(lista[0]["total_pratos"], 2)

    def test_nome_longo_demais(self):
        resposta = self.cliente.post("/api/categorias", json={"nome": "x" * 81})
        self.assertEqual(resposta.status_code, 400)


class PratoTest(BaseApiTest):
    def test_crud_completo(self):
        categoria = self.criar_categoria()
        resposta = self.criar_prato(categoria["id"], descricao="Com farofa")
        self.assertEqual(resposta.status_code, 201)
        prato = resposta.get_json()
        self.assertEqual(prato["categoria_id"], categoria["id"])
        self.assertIs(prato["disponivel"], True)

        lista = self.cliente.get(f"/api/categorias/{categoria['id']}/pratos").get_json()
        self.assertEqual(len(lista), 1)

        resposta = self.cliente.put(
            f"/api/pratos/{prato['id']}", json={"nome": "Feijoada", "preco": "27,50", "disponivel": False}
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json()["preco"], 27.5)
        self.assertIs(resposta.get_json()["disponivel"], False)

        self.assertEqual(self.cliente.delete(f"/api/pratos/{prato['id']}").status_code, 204)
        self.assertEqual(self.cliente.get(f"/api/pratos/{prato['id']}").status_code, 404)

    def test_preco_deve_ser_maior_que_zero(self):
        categoria = self.criar_categoria()
        for preco in [0, -5, "0", "-1,50", 0.004]:
            resposta = self.criar_prato(categoria["id"], preco=preco)
            self.assertEqual(resposta.status_code, 400, preco)
            self.assertIn("maior que zero", resposta.get_json()["campos"]["preco"])

    def test_preco_invalido(self):
        categoria = self.criar_categoria()
        for preco in ["abc", None, "", True, "NaN", "Infinity", 10000]:
            resposta = self.criar_prato(categoria["id"], preco=preco)
            self.assertEqual(resposta.status_code, 400, preco)
            self.assertIn("preco", resposta.get_json()["campos"])

    def test_campos_obrigatorios(self):
        categoria = self.criar_categoria()
        resposta = self.cliente.post(f"/api/categorias/{categoria['id']}/pratos", json={})
        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(set(resposta.get_json()["campos"]), {"nome", "preco"})

    def test_prato_em_categoria_inexistente(self):
        self.assertEqual(self.criar_prato(999).status_code, 404)
        self.assertEqual(self.cliente.get("/api/categorias/999/pratos").status_code, 404)

    def test_disponivel_precisa_ser_booleano(self):
        categoria = self.criar_categoria()
        resposta = self.criar_prato(categoria["id"], disponivel="sim")
        self.assertEqual(resposta.status_code, 400)


class ErrosGeraisTest(BaseApiTest):
    def test_json_invalido(self):
        resposta = self.cliente.post(
            "/api/categorias", data="não é json", content_type="application/json"
        )
        self.assertEqual(resposta.status_code, 400)
        self.assertIn("erro", resposta.get_json())

    def test_rota_inexistente_da_api_responde_json(self):
        resposta = self.cliente.get("/api/nao-existe")
        self.assertEqual(resposta.status_code, 404)
        self.assertEqual(resposta.get_json()["erro"], "Recurso não encontrado.")

    def test_metodo_nao_permitido(self):
        self.assertEqual(self.cliente.patch("/api/categorias").status_code, 405)

    def test_pagina_inicial_e_servida(self):
        self.assertEqual(self.cliente.get("/").status_code, 200)


if __name__ == "__main__":
    unittest.main()
