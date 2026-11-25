"""Endpoints de Prato: listagem/criação por categoria e operações por id."""

from flask import Blueprint, jsonify

from ..database import obter_banco
from ..services import prato_service as servico
from .corpo import ler_corpo_json

blueprint = Blueprint("pratos", __name__, url_prefix="/api")


@blueprint.get("/categorias/<int:categoria_id>/pratos")
def listar_pratos_da_categoria(categoria_id):
    return jsonify(servico.listar_por_categoria(obter_banco(), categoria_id))


@blueprint.post("/categorias/<int:categoria_id>/pratos")
def criar_prato(categoria_id):
    prato = servico.criar(obter_banco(), categoria_id, ler_corpo_json())
    return jsonify(prato), 201


@blueprint.get("/pratos/<int:prato_id>")
def obter_prato(prato_id):
    return jsonify(servico.obter(obter_banco(), prato_id))


@blueprint.put("/pratos/<int:prato_id>")
def atualizar_prato(prato_id):
    return jsonify(servico.atualizar(obter_banco(), prato_id, ler_corpo_json()))


@blueprint.delete("/pratos/<int:prato_id>")
def excluir_prato(prato_id):
    servico.excluir(obter_banco(), prato_id)
    return "", 204
