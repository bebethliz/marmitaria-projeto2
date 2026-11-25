"""Acesso ao banco SQLite: conexão, esquema e ciclo de vida por requisição."""

import sqlite3

from flask import current_app, g

ESQUEMA = """
CREATE TABLE IF NOT EXISTS categoria (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    nome      TEXT NOT NULL UNIQUE COLLATE NOCASE,
    descricao TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS prato (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria_id INTEGER NOT NULL
                 REFERENCES categoria(id) ON DELETE RESTRICT,
    nome         TEXT NOT NULL,
    descricao    TEXT NOT NULL DEFAULT '',
    preco        REAL NOT NULL CHECK (preco > 0),
    disponivel   INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX IF NOT EXISTS idx_prato_categoria ON prato(categoria_id);
"""


def abrir_conexao(caminho):
    conexao = sqlite3.connect(caminho)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_esquema(caminho):
    conexao = abrir_conexao(caminho)
    try:
        conexao.executescript(ESQUEMA)
        conexao.commit()
    finally:
        conexao.close()


def obter_banco():
    """Conexão única por requisição, reaproveitada entre as camadas."""
    if "banco" not in g:
        g.banco = abrir_conexao(current_app.config["DATABASE"])
    return g.banco


def fechar_banco(_erro=None):
    banco = g.pop("banco", None)
    if banco is not None:
        banco.close()
