"""Endpoints de Categoria: /api/categorias."""

from flask import Blueprint, jsonify

from ..database import obter_banco
from ..services import categoria_service as servico
from .corpo import ler_corpo_json

blueprint = Blueprint("categorias", __name__, url_prefix="/api/categorias")


@blueprint.get("")
def listar_categorias():
    return jsonify(servico.listar(obter_banco()))


@blueprint.post("")
def criar_categoria():
    categoria = servico.criar(obter_banco(), ler_corpo_json())
    return jsonify(categoria), 201


@blueprint.get("/<int:categoria_id>")
def obter_categoria(categoria_id):
    return jsonify(servico.obter(obter_banco(), categoria_id))


@blueprint.put("/<int:categoria_id>")
def atualizar_categoria(categoria_id):
    categoria = servico.atualizar(obter_banco(), categoria_id, ler_corpo_json())
    return jsonify(categoria)


@blueprint.delete("/<int:categoria_id>")
def excluir_categoria(categoria_id):
    servico.excluir(obter_banco(), categoria_id)
    return "", 204
