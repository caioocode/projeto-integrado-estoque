import sqlite3
from fastapi import HTTPException
from db.queries.queries import conectar

def deletar_produto_service(id: int):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Pegando o produto para a movimentação de saída
        cursor.execute("SELECT nome, quantidade_estoque FROM produtos WHERE id = ?", (id))
        produto_data = cursor.fetchone()

        if produto_data is None:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        # Deletando o produto
        cursor.execute("DELETE FROM produtos WHERE id = ?", (id))

        # Registrando a movimentação de saída após a exclusão
        cursor.execute('''INSERT INTO movimentacoes (nome_produto, quantidade, preco, tipo_movimentacao)
        VALUES (?, ?, ?, ?)''',
        (produto_data.nome, produto_data.quantidade_estoque, 'saida'))  # produto[1] é a quantidade_estoque

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