"""Regras de negócio de Prato."""

from ..errors import NaoEncontrado
from ..repositories import prato_repository as repositorio
from ..validators import validar_prato
from . import categoria_service


def listar_por_categoria(banco, categoria_id):
    categoria_service.obter(banco, categoria_id)
    return [_para_dicionario(linha) for linha in repositorio.listar_por_categoria(banco, categoria_id)]


def obter(banco, prato_id):
    linha = repositorio.buscar(banco, prato_id)
    if linha is None:
        raise NaoEncontrado("Prato não encontrado.")
    return _para_dicionario(linha)


def criar(banco, categoria_id, dados):
    categoria_service.obter(banco, categoria_id)
    limpo = validar_prato(dados)
    prato_id = repositorio.inserir(banco, categoria_id, limpo)
    banco.commit()
    return obter(banco, prato_id)


def atualizar(banco, prato_id, dados):
    obter(banco, prato_id)
    limpo = validar_prato(dados)
    repositorio.atualizar(banco, prato_id, limpo)
    banco.commit()
    return obter(banco, prato_id)


def excluir(banco, prato_id):
    obter(banco, prato_id)
    repositorio.excluir(banco, prato_id)
    banco.commit()


def _para_dicionario(linha):
    prato = dict(linha)
    prato["disponivel"] = bool(prato["disponivel"])
    return prato
