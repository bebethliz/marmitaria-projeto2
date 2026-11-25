/* Utilitários de interface compartilhados entre as telas. */
const Ui = (() => {
  const CHAVE_MENSAGEM_PENDENTE = "mensagemPendente";
  const DURACAO_TOAST_MS = 4500;
  const formatadorMoeda = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });

  /** Cria elementos via DOM (textContent), evitando injeção de HTML. */
  function el(tag, atributos = {}, ...filhos) {
    const no = document.createElement(tag);
    for (const [chave, valor] of Object.entries(atributos)) {
      if (chave === "class") no.className = valor;
      else if (chave.startsWith("on")) no.addEventListener(chave.slice(2), valor);
      else no.setAttribute(chave, valor);
    }
    for (const filho of filhos.flat()) {
      if (filho !== null && filho !== undefined) no.append(filho);
    }
    return no;
  }

  function toast(mensagem, tipo = "sucesso") {
    const caixa = el("div", { class: `toast toast-${tipo}`, role: "status" }, mensagem);
    document.getElementById("toasts").append(caixa);
    setTimeout(() => caixa.remove(), DURACAO_TOAST_MS);
  }

  /** Guarda uma mensagem para ser exibida na próxima tela (após redirecionar). */
  function lembrarMensagem(mensagem) {
    sessionStorage.setItem(CHAVE_MENSAGEM_PENDENTE, mensagem);
  }

  function exibirMensagemPendente() {
    const mensagem = sessionStorage.getItem(CHAVE_MENSAGEM_PENDENTE);
    if (!mensagem) return;
    sessionStorage.removeItem(CHAVE_MENSAGEM_PENDENTE);
    toast(mensagem);
  }

  function formatarPreco(valor) {
    return formatadorMoeda.format(valor);
  }

  function formatarPrecoParaCampo(valor) {
    return Number(valor).toFixed(2).replace(".", ",");
  }

  function parametro(nome) {
    return new URLSearchParams(window.location.search).get(nome);
  }

  function limparErros(formulario) {
    formulario.querySelectorAll("[data-erro-de]").forEach((p) => (p.textContent = ""));
    formulario.querySelectorAll("[aria-invalid]").forEach((campo) => campo.removeAttribute("aria-invalid"));
  }

  function mostrarErrosDosCampos(formulario, campos) {
    for (const [nome, mensagem] of Object.entries(campos)) {
      const campo = formulario.elements[nome];
      const area = formulario.querySelector(`[data-erro-de="${nome}"]`);
      if (campo) campo.setAttribute("aria-invalid", "true");
      if (area) area.textContent = mensagem;
    }
    const primeiro = Object.keys(campos).map((nome) => formulario.elements[nome]).find(Boolean);
    if (primeiro) primeiro.focus();
  }

  /** Mostra o erro de um envio: por campo, quando o servidor detalha, e sempre em um aviso. */
  function tratarErroDeEnvio(formulario, erro) {
    if (erro.campos && Object.keys(erro.campos).length > 0) {
      mostrarErrosDosCampos(formulario, erro.campos);
    }
    toast(erro.message, "erro");
  }

  function renderizarCabecalho() {
    const cabecalho = document.getElementById("cabecalho");
    if (!cabecalho) return;
    cabecalho.append(
      el("a", { class: "marca", href: "index.html" }, "Sabor de Casa", el("small", {}, "Cardápio digital")),
      el("nav", {}, el("a", { href: "index.html" }, "Categorias"))
    );
  }

  document.addEventListener("DOMContentLoaded", () => {
    renderizarCabecalho();
    exibirMensagemPendente();
  });

  return {
    el, toast, lembrarMensagem, formatarPreco, formatarPrecoParaCampo,
    parametro, limparErros, mostrarErrosDosCampos, tratarErroDeEnvio,
  };
})();
