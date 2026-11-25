/* Tela: lista de pratos de uma categoria (?categoria=N). */
const categoriaId = Ui.parametro("categoria");
const corpoTabela = document.getElementById("lista-pratos");
const estadoVazio = document.getElementById("estado-vazio");

function criarEtiquetaDeSituacao(prato) {
  return prato.disponivel
    ? Ui.el("span", { class: "etiqueta etiqueta-ok" }, "Disponível")
    : Ui.el("span", { class: "etiqueta etiqueta-off" }, "Indisponível");
}

function criarLinha(prato) {
  const { el } = Ui;
  return el(
    "tr",
    {},
    el("td", {}, el("strong", {}, prato.nome)),
    el("td", { class: "descricao-celula" }, prato.descricao || "—"),
    el("td", { class: "numero" }, Ui.formatarPreco(prato.preco)),
    el("td", {}, criarEtiquetaDeSituacao(prato)),
    el(
      "td",
      { class: "acoes" },
      el("a", { class: "botao botao-pequeno", href: `prato-form.html?id=${prato.id}` }, "Editar"),
      el("button", { class: "botao botao-pequeno botao-perigo", type: "button", onclick: () => excluirPrato(prato) }, "Excluir")
    )
  );
}

function renderizarPratos(pratos) {
  corpoTabela.replaceChildren(...pratos.map(criarLinha));
  estadoVazio.hidden = pratos.length > 0;
}

function preencherCabecalho(categoria) {
  document.getElementById("titulo").textContent = categoria.nome;
  document.getElementById("migalha-atual").textContent = categoria.nome;
  document.getElementById("subtitulo").textContent = categoria.descricao || "Pratos desta categoria.";
  document.getElementById("botao-novo").href = `prato-form.html?categoria=${categoria.id}`;
}

async function carregarTela() {
  try {
    const [categoria, pratos] = await Promise.all([
      Api.categorias.obter(categoriaId),
      Api.pratos.listarDaCategoria(categoriaId),
    ]);
    preencherCabecalho(categoria);
    renderizarPratos(pratos);
  } catch (erro) {
    Ui.lembrarMensagem(erro.message);
    window.location.href = "index.html";
  }
}

async function excluirPrato(prato) {
  if (!confirm(`Excluir o prato "${prato.nome}"?`)) return;
  try {
    await Api.pratos.excluir(prato.id);
    Ui.toast("Prato excluído com sucesso.");
    renderizarPratos(await Api.pratos.listarDaCategoria(categoriaId));
  } catch (erro) {
    Ui.toast(erro.message, "erro");
  }
}

if (categoriaId) {
  carregarTela();
} else {
  window.location.href = "index.html";
}
