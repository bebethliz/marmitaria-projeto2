"""Validação de entrada. Devolve dados limpos ou lança ErroDeValidacao."""

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from .errors import ErroDeValidacao

TAMANHO_MAXIMO_NOME = 80
TAMANHO_MAXIMO_DESCRICAO = 200
PRECO_MAXIMO = Decimal("9999.99")
CENTAVO = Decimal("0.01")


def _ler_texto(dados, campo, rotulo, erros, obrigatorio, tamanho_maximo):
    valor = dados.get(campo)
    if valor is None:
        valor = ""
    if not isinstance(valor, str):
        erros[campo] = f"{rotulo} deve ser um texto."
        return ""
    valor = valor.strip()
    if obrigatorio and not valor:
        erros[campo] = f"{rotulo} é obrigatório."
    elif len(valor) > tamanho_maximo:
        erros[campo] = f"{rotulo} deve ter no máximo {tamanho_maximo} caracteres."
    return valor


def _ler_preco(dados, erros):
    bruto = dados.get("preco")
    if bruto is None or (isinstance(bruto, str) and not bruto.strip()):
        erros["preco"] = "Preço é obrigatório."
        return None
    try:
        if isinstance(bruto, bool):
            raise InvalidOperation
        valor = Decimal(str(bruto).strip().replace(",", "."))
    except InvalidOperation:
        erros["preco"] = "Preço deve ser um número válido."
        return None
    if not valor.is_finite():
        erros["preco"] = "Preço deve ser um número válido."
        return None
    if valor <= 0:
        erros["preco"] = "Preço deve ser maior que zero."
        return None
    if valor > PRECO_MAXIMO:
        erros["preco"] = "Preço não pode ultrapassar R$ 9.999,99."
        return None
    arredondado = valor.quantize(CENTAVO, rounding=ROUND_HALF_UP)
    if arredondado <= 0:
        erros["preco"] = "Preço deve ser maior que zero."
        return None
    return float(arredondado)


def _ler_booleano(dados, campo, rotulo, erros, padrao):
    valor = dados.get(campo, padrao)
    if not isinstance(valor, bool):
        erros[campo] = f"{rotulo} deve ser verdadeiro ou falso."
        return padrao
    return valor


def _lancar_se_houver_erros(erros):
    if erros:
        raise ErroDeValidacao("Há campos inválidos. Corrija e tente novamente.", erros)


def validar_categoria(dados):
    erros = {}
    limpo = {
        "nome": _ler_texto(dados, "nome", "Nome", erros, True, TAMANHO_MAXIMO_NOME),
        "descricao": _ler_texto(
            dados, "descricao", "Descrição", erros, False, TAMANHO_MAXIMO_DESCRICAO
        ),
    }
    _lancar_se_houver_erros(erros)
    return limpo


def validar_prato(dados):
    erros = {}
    limpo = {
        "nome": _ler_texto(dados, "nome", "Nome", erros, True, TAMANHO_MAXIMO_NOME),
        "descricao": _ler_texto(
            dados, "descricao", "Descrição", erros, False, TAMANHO_MAXIMO_DESCRICAO
        ),
        "preco": _ler_preco(dados, erros),
        "disponivel": _ler_booleano(dados, "disponivel", "Disponibilidade", erros, True),
    }
    _lancar_se_houver_erros(erros)
    return limpo
