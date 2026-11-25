"""Camada de interface HTTP: converte requisições em chamadas de serviço."""

from . import categorias, pratos


def registrar_rotas(app):
    app.register_blueprint(categorias.blueprint)
    app.register_blueprint(pratos.blueprint)
