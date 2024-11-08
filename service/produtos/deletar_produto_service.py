import sqlite3
from fastapi import HTTPException
from db.queries.queries import conectar

def deletar_produto_service(nome: str):
    try:

        conexao = conectar()
        cursor = conexao.cursor()

        # Pegando o produto para a movimentação de saída
        cursor.execute("SELECT nome, quantidade_estoque FROM produtos WHERE nome = ?", (nome,))
        produto = cursor.fetchone()

        if produto is None:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        # Deletando o produto
        cursor.execute("DELETE FROM produtos WHERE nome = ?", (nome,))

        # Registrando a movimentação de saída após a exclusão
        cursor.execute('''INSERT INTO movimentacoes (nome_produto, quantidade, preco, tipo_movimentacao)
        VALUES (?, ?, ?, ?)''',
        (nome, produto[1], 'saida'))  # produto[1] é a quantidade_estoque

        conexao.commit()
        conexao.close()
    except sqlite3.IntegrityError as e:
        # Caso haja erro de integridade (ex: chave única duplicada)
        raise ValueError("Erro de integridade no banco de dados: " + str(e))
    except sqlite3.OperationalError as e:
        # Erro operacional, como erro de SQL ou banco de dados não encontrado
        raise sqlite3.DatabaseError("Erro operacional no banco de dados: " + str(e))
    except Exception as e:
        # Erros gerais de exceção
        raise Exception("Erro ao processar a solicitação: " + str(e))