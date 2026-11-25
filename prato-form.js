/* Tela: cadastro/edição de prato.
   ?categoria=N cria um prato novo na categoria N; ?id=N edita o prato N. */
const formulario = document.getElementById("formulario");
const botaoSalvar = document.getElementById("botao-salvar");
const pratoId = Ui.parametro("id");
let categoriaId = Ui.parametro("categoria");

function lerFormulario() {
  return {
    nome: formulario.elements.nome.value.trim(),
    descricao: formulario.elements.descricao.value.trim(),
    preco: Validacao.converterPreco(formulario.elements.preco.value),
    disponivel: formulario.elements.disponivel.checked,
  };
}

function lerPrecoDigitado() {
  return formulario.elements.preco.value.trim() === "" ? "" : Validacao.converterPreco(formulario.elements.preco.value);
}

function urlDaListaDePratos() {
  return `pratos.html?categoria=${categoriaId}`;
}

function atualizarNavegacao(categoria) {
  const link = document.getElementById("migalha-categoria");
  link.textContent = categoria.nome;
  link.href = urlDaListaDePratos();
  document.getElementById("botao-cancelar").href = urlDaListaDePratos();
}

function preencherFormulario(prato) {
  formulario.elements.nome.value = prato.nome;
  formulario.elements.descricao.value = prato.descricao;
  formulario.elements.preco.value = Ui.formatarPrecoParaCampo(prato.preco);
  formulario.elements.disponivel.checked = prato.disponivel;
  document.getElementById("titulo").textContent = "Editar prato";
  document.getElementById("migalha-atual").textContent = prato.nome;
}

async function carregarTela() {
  try {
    if (pratoId) {
      const prato = await Api.pratos.obter(pratoId);
      categoriaId = prato.categoria_id;
      preencherFormulario(prato);
    }
    atualizarNavegacao(await Api.categorias.obter(categoriaId));
  } catch (erro) {
    Ui.lembrarMensagem(erro.message);
    window.location.href = "index.html";
  }
}

async function enviar(evento) {
  evento.preventDefault();
  Ui.limparErros(formulario);

  const dados = lerFormulario();
  const erros = Validacao.validarPrato({ ...dados, preco: lerPrecoDigitado() });
  if (Object.keys(erros).length > 0) {
    Ui.mostrarErrosDosCampos(formulario, erros);
    return;
  }

  botaoSalvar.disabled = true;
  try {
    if (pratoId) await Api.pratos.atualizar(pratoId, dados);
    else await Api.pratos.criar(categoriaId, dados);
    Ui.lembrarMensagem("Prato salvo com sucesso.");
    window.location.href = urlDaListaDePratos();
  } catch (erro) {
    Ui.tratarErroDeEnvio(formulario, erro);
    botaoSalvar.disabled = false;
  }
}

formulario.addEventListener("submit", enviar);
if (pratoId || categoriaId) {
  carregarTela();
} else {
  window.location.href = "index.html";
}
