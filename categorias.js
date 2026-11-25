/* Tela: lista de categorias. */
const corpoTabela = document.getElementById("lista-categorias");
const estadoVazio = document.getElementById("estado-vazio");

function criarLinha(categoria) {
  const { el } = Ui;
  return el(
    "tr",
    {},
    el("td", {}, el("strong", {}, categoria.nome)),
    el("td", { class: "descricao-celula" }, categoria.descricao || "—"),
    el("td", { class: "numero" }, String(categoria.total_pratos)),
    el(
      "td",
      { class: "acoes" },
      el("a", { class: "botao botao-pequeno", href: `pratos.html?categoria=${categoria.id}` }, "Ver pratos"),
      el("a", { class: "botao botao-pequeno", href: `categoria-form.html?id=${categoria.id}` }, "Editar"),
      el("button", { class: "botao botao-pequeno botao-perigo", type: "button", onclick: () => excluirCategoria(categoria) }, "Excluir")
    )
  );
}

function renderizar(categorias) {
  corpoTabela.replaceChildren(...categorias.map(criarLinha));
  estadoVazio.hidden = categorias.length > 0;
}

async function carregarCategorias() {
  try {
    renderizar(await Api.categorias.listar());
  } catch (erro) {
    Ui.toast(erro.message, "erro");
  }
}

async function excluirCategoria(categoria) {
  if (!confirm(`Excluir a categoria "${categoria.nome}"?`)) return;
  try {
    await Api.categorias.excluir(categoria.id);
    Ui.toast("Categoria excluída com sucesso.");
    await carregarCategorias();
  } catch (erro) {
    Ui.toast(erro.message, "erro");
  }
}

carregarCategorias();
