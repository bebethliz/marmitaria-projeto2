/* Cliente do serviço Web: única camada que conhece URLs e formato HTTP. */
const Api = (() => {
  const PREFIXO = "/api";

  class ErroApi extends Error {
    constructor(mensagem, status, campos) {
      super(mensagem);
      this.status = status;
      this.campos = campos || {};
    }
  }

  async function requisitar(metodo, caminho, corpo) {
    const opcoes = { method: metodo, headers: {} };
    if (corpo !== undefined) {
      opcoes.headers["Content-Type"] = "application/json";
      opcoes.body = JSON.stringify(corpo);
    }

    let resposta;
    try {
      resposta = await fetch(PREFIXO + caminho, opcoes);
    } catch {
      throw new ErroApi("Não foi possível conectar ao servidor. Verifique sua conexão.", 0);
    }

    if (resposta.status === 204) return null;
    const dados = await resposta.json().catch(() => null);
    if (!resposta.ok) {
      throw new ErroApi(dados?.erro || "Ocorreu um erro inesperado.", resposta.status, dados?.campos);
    }
    return dados;
  }

  const categorias = {
    listar: () => requisitar("GET", "/categorias"),
    obter: (id) => requisitar("GET", `/categorias/${id}`),
    criar: (dados) => requisitar("POST", "/categorias", dados),
    atualizar: (id, dados) => requisitar("PUT", `/categorias/${id}`, dados),
    excluir: (id) => requisitar("DELETE", `/categorias/${id}`),
  };

  const pratos = {
    listarDaCategoria: (categoriaId) => requisitar("GET", `/categorias/${categoriaId}/pratos`),
    obter: (id) => requisitar("GET", `/pratos/${id}`),
    criar: (categoriaId, dados) => requisitar("POST", `/categorias/${categoriaId}/pratos`, dados),
    atualizar: (id, dados) => requisitar("PUT", `/pratos/${id}`, dados),
    excluir: (id) => requisitar("DELETE", `/pratos/${id}`),
  };

  return { ErroApi, categorias, pratos };
})();
