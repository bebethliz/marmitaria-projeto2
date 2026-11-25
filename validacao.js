/* Validação no navegador (feedback imediato). O servidor valida de novo: é a fonte da verdade. */
const Validacao = (() => {
  const TAMANHO_MAXIMO_NOME = 80;
  const TAMANHO_MAXIMO_DESCRICAO = 200;
  const PRECO_MAXIMO = 9999.99;

  function validarTexto(erros, campo, rotulo, valor, obrigatorio, tamanhoMaximo) {
    if (obrigatorio && !valor) erros[campo] = `${rotulo} é obrigatório.`;
    else if (valor.length > tamanhoMaximo) erros[campo] = `${rotulo} deve ter no máximo ${tamanhoMaximo} caracteres.`;
  }

  function converterPreco(texto) {
    const normalizado = texto.trim().replace(",", ".");
    return normalizado === "" ? NaN : Number(normalizado);
  }

  function validarCategoria(dados) {
    const erros = {};
    validarTexto(erros, "nome", "Nome", dados.nome, true, TAMANHO_MAXIMO_NOME);
    validarTexto(erros, "descricao", "Descrição", dados.descricao, false, TAMANHO_MAXIMO_DESCRICAO);
    return erros;
  }

  function validarPrato(dados) {
    const erros = {};
    validarTexto(erros, "nome", "Nome", dados.nome, true, TAMANHO_MAXIMO_NOME);
    validarTexto(erros, "descricao", "Descrição", dados.descricao, false, TAMANHO_MAXIMO_DESCRICAO);
    if (dados.preco === "") erros.preco = "Preço é obrigatório.";
    else if (!Number.isFinite(dados.preco)) erros.preco = "Preço deve ser um número válido.";
    else if (dados.preco <= 0) erros.preco = "Preço deve ser maior que zero.";
    else if (dados.preco > PRECO_MAXIMO) erros.preco = "Preço não pode ultrapassar R$ 9.999,99.";
    return erros;
  }

  return { validarCategoria, validarPrato, converterPreco };
})();
