"""Consultas SQL da entidade Categoria. Não faz commit: isso é do serviço."""


def listar(banco):
    return banco.execute(
        """
        SELECT c.id, c.nome, c.descricao, COUNT(p.id) AS total_pratos
          FROM categoria c
          LEFT JOIN prato p ON p.categoria_id = c.id
         GROUP BY c.id
         ORDER BY c.nome
        """
    ).fetchall()


def buscar(banco, categoria_id):
    return banco.execute(
        """
        SELECT c.id, c.nome, c.descricao,
               (SELECT COUNT(*) FROM prato p WHERE p.categoria_id = c.id) AS total_pratos
          FROM categoria c
         WHERE c.id = ?
        """,
        (categoria_id,),
    ).fetchone()


def buscar_id_por_nome(banco, nome):
    """O índice UNIQUE COLLATE NOCASE ignora maiúsculas/minúsculas."""
    linha = banco.execute("SELECT id FROM categoria WHERE nome = ?", (nome,)).fetchone()
    return linha["id"] if linha else None


def inserir(banco, dados):
    cursor = banco.execute(
        "INSERT INTO categoria (nome, descricao) VALUES (?, ?)",
        (dados["nome"], dados["descricao"]),
    )
    return cursor.lastrowid


def atualizar(banco, categoria_id, dados):
    banco.execute(
        "UPDATE categoria SET nome = ?, descricao = ? WHERE id = ?",
        (dados["nome"], dados["descricao"], categoria_id),
    )


def contar_pratos(banco, categoria_id):
    return banco.execute(
        "SELECT COUNT(*) FROM prato WHERE categoria_id = ?", (categoria_id,)
    ).fetchone()[0]


def excluir(banco, categoria_id):
    banco.execute("DELETE FROM categoria WHERE id = ?", (categoria_id,))
