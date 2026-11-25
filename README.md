# Sabor de Casa — Cardápio digital (Cenário 3: Marmitaria)

Aplicação Web para a marmitaria **Sabor de Casa** manter o cardápio organizado por **categorias**
e **pratos**. Interface em HTML/CSS/JS que consome um serviço Web próprio (API REST em Flask)
com persistência em banco de dados SQLite.

- **Aplicação publicada:** _(colar o link aqui após publicar)_
- **Repositório:** _(colar o link do GitHub aqui)_

## Entidades

| Entidade  | Campos                                              | Relação                                  |
|-----------|-----------------------------------------------------|------------------------------------------|
| Categoria | `id`, `nome` (único), `descricao`                   | 1 categoria → N pratos                   |
| Prato     | `id`, `categoria_id`, `nome`, `descricao`, `preco`, `disponivel` | cada prato pertence a 1 categoria |

## Como rodar localmente

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python wsgi.py                                       # http://localhost:5000
python -m unittest discover -s . -t . -v             # testes automatizados (18)
```

Variáveis opcionais: `PORT` (padrão 5000), `DATABASE_PATH` (padrão `marmitaria.db`),
`SEED_DEMO=0` para não inserir o cardápio de demonstração quando o banco está vazio.

## Arquitetura (separação em camadas)

```
frontend/                    INTERFACE  (HTML + CSS + JS puro)
  *.html                     4 telas: lista de categorias, form de categoria,
                             lista de pratos, form de prato
  js/api.js                  único ponto que conhece URLs/HTTP da API
  js/validacao.js            validação no navegador (feedback imediato)
  js/ui.js                   utilitários de tela (DOM seguro, avisos, formatação)
backend/
  routes/                    SERVIÇO – HTTP: converte requisição em chamada de serviço
  services/                  SERVIÇO – regras de negócio e transações
  validators.py              validação de entrada (fonte da verdade)
  repositories/              DADOS – único lugar com SQL
  database.py                conexão e esquema SQLite
  errors.py                  erros da aplicação → respostas JSON padronizadas
app.py / wsgi.py             montagem da aplicação / ponto de entrada
tests/test_api.py            testes da API
```

## API

| Método | Rota                              | Descrição                         | Sucesso |
|--------|-----------------------------------|-----------------------------------|---------|
| GET    | `/api/categorias`                 | lista categorias (com `total_pratos`) | 200 |
| POST   | `/api/categorias`                 | cria categoria                    | 201 |
| GET    | `/api/categorias/{id}`            | obtém categoria                   | 200 |
| PUT    | `/api/categorias/{id}`            | atualiza categoria                | 200 |
| DELETE | `/api/categorias/{id}`            | exclui (bloqueado se tiver pratos)| 204 |
| GET    | `/api/categorias/{id}/pratos`     | lista pratos da categoria         | 200 |
| POST   | `/api/categorias/{id}/pratos`     | cria prato na categoria           | 201 |
| GET    | `/api/pratos/{id}`                | obtém prato                       | 200 |
| PUT    | `/api/pratos/{id}`                | atualiza prato                    | 200 |
| DELETE | `/api/pratos/{id}`                | exclui prato                      | 204 |

Erros seguem sempre o formato `{"erro": "mensagem", "campos": {"campo": "mensagem"}}`
com status **400** (validação), **404** (não encontrado) ou **409** (regra de negócio).

Exemplo:

```bash
curl -X POST http://localhost:5000/api/categorias/1/pratos \
     -H "Content-Type: application/json" \
     -d '{"nome":"Feijão tropeiro","preco":"25,50","disponivel":true}'
```

## Regras de validação (cenário 3)

| Regra do enunciado                          | Onde está implementada                                              |
|---------------------------------------------|---------------------------------------------------------------------|
| Campos obrigatórios                         | `backend/validators.py` e `frontend/js/validacao.js`                |
| Preço maior que zero                        | `validators._ler_preco` + `CHECK (preco > 0)` no banco              |
| Nome de categoria sem repetição             | `categoria_service._garantir_nome_livre` + `UNIQUE COLLATE NOCASE` no banco (ignora maiúsculas/minúsculas) |
| Impedir exclusão de categoria com pratos    | `categoria_service.excluir` + `ON DELETE RESTRICT` no banco         |

As regras críticas existem **também no banco**: mesmo que alguém chame a API de outra forma, os dados
continuam consistentes. O nome da categoria é comparado após remover espaços nas pontas.

## Persistência

Banco de dados **SQLite** (módulo `sqlite3` da biblioteca padrão), com chave estrangeira entre
`prato.categoria_id` e `categoria.id` (`PRAGMA foreign_keys = ON`). O esquema é criado
automaticamente na primeira execução (`backend/database.py`).

## Clean code — onde mostrar cada prática no PDF

Ao montar o PDF, aponte links do GitHub (não cole código) para:

| Prática                         | Evidência no repositório                                                        |
|---------------------------------|----------------------------------------------------------------------------------|
| Nomes significativos            | `backend/services/categoria_service.py` (`_garantir_nome_livre`, `excluir`)     |
| Funções curtas, 1 responsabilidade | `backend/validators.py` (`_ler_texto`, `_ler_preco`, `_ler_booleano`)        |
| Separação em camadas            | pastas `routes/` → `services/` → `repositories/` e `frontend/js/api.js`          |
| Sem código duplicado            | `backend/routes/corpo.py` (leitura de JSON), `frontend/js/ui.js` (`el`, `tratarErroDeEnvio`) |

## Publicação (exemplo: Render)

1. Suba o projeto para um repositório **público** no GitHub.
2. No Render, crie um *Web Service* a partir do repositório (o `render.yaml` já tem a configuração:
   build `pip install -r requirements.txt`, start `gunicorn wsgi:app`).
3. Abra o link gerado, teste as 4 telas e anote o endereço neste README e no PDF.

> **Atenção:** em planos gratuitos o disco da hospedagem costuma ser **efêmero** — o arquivo SQLite
> volta ao estado inicial a cada novo deploy/reinício (o cardápio de demonstração é recriado
> automaticamente). Para dados que sobrevivem, use disco persistente (`DATABASE_PATH` apontando para ele)
> ou um banco gerenciado. O prazo exige a aplicação e o repositório acessíveis até **10/12**.

## Evidências para o PDF

A pasta `docs/evidencias/` contém capturas de tela geradas com a aplicação rodando (lista, formulários,
erros de validação, exclusão bloqueada, edição e visão mobile). Recomenda-se **refazer as capturas
na aplicação publicada** para que a URL real apareça. Para evidenciar requisições e respostas da API,
use o `curl` do exemplo acima ou a aba *Rede* do navegador.

## Uso de IA generativa (declaração obrigatória)

> Este projeto foi desenvolvido com apoio de IA generativa (Claude, da Anthropic) na geração inicial
> do código e dos testes. A equipe revisou, executou e compreende todo o código entregue e responde por ele.

_Ajuste o texto conforme o uso real da equipe. Todos os integrantes devem conseguir explicar cada camada
(rotas, serviços, repositórios, validação e interface)._
