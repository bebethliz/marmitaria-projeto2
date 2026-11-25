"""Leitura segura do corpo JSON das requisições."""

from flask import request

from ..errors import ErroDeValidacao


def ler_corpo_json():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        raise ErroDeValidacao("O corpo da requisição deve ser um objeto JSON válido.")
    return dados
