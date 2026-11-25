"""Fábrica da aplicação Flask: monta banco, rotas, tratadores de erro e frontend."""

import os
from pathlib import Path

from flask import Flask

from backend.database import criar_esquema, fechar_banco
from backend.errors import registrar_tratadores
from backend.routes import registrar_rotas
from backend.seed import semear_se_vazio

RAIZ = Path(__file__).resolve().parent


def create_app(caminho_banco=None, semear=None):
    app = Flask(__name__, static_folder="frontend", static_url_path="")
    app.config["DATABASE"] = caminho_banco or os.environ.get(
        "DATABASE_PATH", str(RAIZ / "marmitaria.db")
    )

    criar_esquema(app.config["DATABASE"])
    if semear is None:
        semear = os.environ.get("SEED_DEMO", "1") == "1"
    if semear:
        semear_se_vazio(app.config["DATABASE"])

    app.teardown_appcontext(fechar_banco)
    registrar_tratadores(app)
    registrar_rotas(app)

    @app.get("/")
    def pagina_inicial():
        return app.send_static_file("index.html")

    return app
