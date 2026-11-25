"""Dados de demonstração, inseridos apenas quando o banco está vazio."""

from .database import abrir_conexao
from .repositories import categoria_repository, prato_repository

CARDAPIO_DEMO = {
    "Marmitas Tradicionais": [
        ("Feijoada completa", "Feijão preto, arroz, couve, farofa e laranja.", 24.90, True),
        ("Frango grelhado com purê", "Filé de frango, purê de batata e salada.", 22.00, True),
        ("Strogonoff de frango", "Acompanha arroz branco e batata palha.", 23.50, True),
    ],
    "Marmitas Fit": [
        ("Tilápia com legumes", "Tilápia assada, legumes no vapor e arroz integral.", 26.00, True),
        ("Omelete de forno com salada", "Omelete de forno com folhas e tomate.", 19.90, False),
    ],
    "Bebidas": [
        ("Suco natural 500 ml", "Sabores do dia: laranja, maracujá ou acerola.", 8.00, True),
        ("Refrigerante lata", "Lata de 350 ml.", 6.00, True),
    ],
    "Sobremesas": [
        ("Pudim de leite", "Porção individual com calda de caramelo.", 9.50, True),
    ],
}


def semear_se_vazio(caminho_banco):
    banco = abrir_conexao(caminho_banco)
    try:
        if categoria_repository.listar(banco):
            return
        for nome_categoria, pratos in CARDAPIO_DEMO.items():
            categoria_id = categoria_repository.inserir(
                banco, {"nome": nome_categoria, "descricao": ""}
            )
            for nome, descricao, preco, disponivel in pratos:
                prato_repository.inserir(
                    banco,
                    categoria_id,
                    {"nome": nome, "descricao": descricao, "preco": preco, "disponivel": disponivel},
                )
        banco.commit()
    finally:
        banco.close()
