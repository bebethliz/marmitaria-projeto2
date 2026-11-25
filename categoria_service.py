"""Regras de negócio de Categoria."""

import sqlite3

from ..errors import ErroDeNegocio, NaoEncontrado
from ..repositories import categoria_repository as repositorio
from ..validators import validar_categoria

MENSAGEM_NOME_REPETIDO = "Já existe uma categoria com este nome."


def listar(banco):
    return [dict(linha) for linha in repositorio.listar(banco)]


def obter(banco, categoria_id):
    linha = repositorio.buscar(banco, categoria_id)
    if linha is None:
        raise NaoEncontrado("Categoria não encontrada.")
    return dict(linha)


def criar(banco, dados):
    limpo = validar_categoria(dados)
    _garantir_nome_livre(banco, limpo["nome"])
    categoria_id = _gravar(banco, lambda: repositorio.inserir(banco, limpo))
    return obter(banco, categoria_id)


def atualizar(banco, categoria_id, dados):
    obter(banco, categoria_id)
    limpo = validar_categoria(dados)
    _garantir_nome_livre(banco, limpo["nome"], ignorar_id=categoria_id)
    _gravar(banco, lambda: repositorio.atualizar(banco, categoria_id, limpo))
    return obter(banco, categoria_id)


def excluir(banco, categoria_id):
    obter(banco, categoria_id)
    total = repositorio.contar_pratos(banco, categoria_id)
    if total > 0:
        raise ErroDeNegocio(
            f"Não é possível excluir: a categoria ainda possui {total} prato(s). "
            "Exclua ou mova os pratos antes."
        )
    repositorio.excluir(banco, categoria_id)
    banco.commit()


def _garantir_nome_livre(banco, nome, ignorar_id=None):
    existente = repositorio.buscar_id_por_nome(banco, nome)
    if existente is not None and existente != ignorar_id:
        raise ErroDeNegocio(MENSAGEM_NOME_REPETIDO, {"nome": MENSAGEM_NOME_REPETIDO})


def _gravar(banco, operacao):
    """Executa a gravação; o índice UNIQUE cobre a corrida entre requisições."""
    try:
        resultado = operacao()
        banco.commit()
        return resultado
    except sqlite3.IntegrityError as erro:
        banco.rollback()
        raise ErroDeNegocio(MENSAGEM_NOME_REPETIDO, {"nome": MENSAGEM_NOME_REPETIDO}) from erro
