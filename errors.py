"""Erros da aplicação e conversão deles em respostas JSON padronizadas."""

from flask import jsonify, request
from werkzeug.exceptions import HTTPException

MENSAGENS_HTTP = {
    404: "Recurso não encontrado.",
    405: "Método não permitido para este recurso.",
}


class ErroDeAplicacao(Exception):
    """Base dos erros esperados; cada subclasse define o status HTTP."""

    status = 500

    def __init__(self, mensagem, campos=None):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.campos = campos or {}


class ErroDeValidacao(ErroDeAplicacao):
    status = 400


class NaoEncontrado(ErroDeAplicacao):
    status = 404


class ErroDeNegocio(ErroDeAplicacao):
    """Violação de regra de negócio (ex.: nome repetido, exclusão bloqueada)."""

    status = 409


def _resposta_de_erro(mensagem, status, campos=None):
    corpo = {"erro": mensagem}
    if campos:
        corpo["campos"] = campos
    return jsonify(corpo), status


def registrar_tratadores(app):
    @app.errorhandler(ErroDeAplicacao)
    def tratar_erro_da_aplicacao(erro):
        return _resposta_de_erro(erro.mensagem, erro.status, erro.campos)

    @app.errorhandler(HTTPException)
    def tratar_erro_http(erro):
        if not request.path.startswith("/api/"):
            return erro
        mensagem = MENSAGENS_HTTP.get(erro.code, erro.description)
        return _resposta_de_erro(mensagem, erro.code)

    @app.errorhandler(Exception)
    def tratar_erro_inesperado(erro):
        app.logger.exception("Erro inesperado: %s", erro)
        return _resposta_de_erro("Erro interno do servidor. Tente novamente.", 500)
