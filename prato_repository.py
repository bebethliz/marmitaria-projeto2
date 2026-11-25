"""Consultas SQL da entidade Prato. Não faz commit: isso é do serviço."""

COLUNAS = "id, categoria_id, nome, descricao, preco, disponivel"


def listar_por_categoria(banco, categoria_id):
    return banco.execute(
        f"SELECT {COLUNAS} FROM prato WHERE categoria_id = ? ORDER BY nome",
        (categoria_id,),
    ).fetchall()


def buscar(banco, prato_id):
    return banco.execute(
        f"SELECT {COLUNAS} FROM prato WHERE id = ?", (prato_id,)
    ).fetchone()


def inserir(banco, categoria_id, dados):
    cursor = banco.execute(
        """
        INSERT INTO prato (categoria_id, nome, descricao, preco, disponivel)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            categoria_id,
            dados["nome"],
            dados["descricao"],
            dados["preco"],
            int(dados["disponivel"]),
        ),
    )
    return cursor.lastrowid


def atualizar(banco, prato_id, dados):
    banco.execute(
        """
        UPDATE prato
           SET nome = ?, descricao = ?, preco = ?, disponivel = ?
         WHERE id = ?
        """,
        (
            dados["nome"],
            dados["descricao"],
            dados["preco"],
            int(dados["disponivel"]),
            prato_id,
        ),
    )


def excluir(banco, prato_id):
    banco.execute("DELETE FROM prato WHERE id = ?", (prato_id,))
