/* Tela: cadastro/edição de categoria. Com ?id=N edita; sem id, cria. */
const formulario = document.getElementById("formulario");
const botaoSalvar = document.getElementById("botao-salvar");
const categoriaId = Ui.parametro("id");

function lerFormulario() {
  return {
    nome: formulario.elements.nome.value.trim(),
    descricao: formulario.elements.descricao.value.trim(),
  };
}

function preencherFormulario(categoria) {
  formulario.elements.nome.value = categoria.nome;
  formulario.elements.descricao.value = categoria.descricao;
  document.getElementById("titulo").textContent = "Editar categoria";
  document.getElementById("migalha-atual").textContent = categoria.nome;
}

async function carregarCategoria() {
  try {
    preencherFormulario(await Api.categorias.obter(categoriaId));
  } catch (erro) {
    Ui.lembrarMensagem(erro.message);
    window.location.href = "index.html";
  }
}

async function enviar(evento) {
  evento.preventDefault();
  Ui.limparErros(formulario);

  const dados = lerFormulario();
  const erros = Validacao.validarCategoria(dados);
  if (Object.keys(erros).length > 0) {
    Ui.mostrarErrosDosCampos(formulario, erros);
    return;
  }

  botaoSalvar.disabled = true;
  try {
    if (categoriaId) await Api.categorias.atualizar(categoriaId, dados);
    else await Api.categorias.criar(dados);
    Ui.lembrarMensagem("Categoria salva com sucesso.");
    window.location.href = "index.html";
  } catch (erro) {
    Ui.tratarErroDeEnvio(formulario, erro);
    botaoSalvar.disabled = false;
  }
}

formulario.addEventListener("submit", enviar);
if (categoriaId) carregarCategoria();
