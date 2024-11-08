import sqlite3
from fastapi import HTTPException
from db.queries.queries import conectar

def gerar_relatorio_service(nome: str):
    try:

        conexao = conectar()
        cursor = conexao.cursor()

        # Consultando as movimentações do produto
        cursor.execute('''SELECT * FROM movimentacoes WHERE nome_produto = ? ORDER BY data_movimentacao DESC''',
                       (nome,))
        movimentacoes = cursor.fetchall()

        conexao.close()

        if not movimentacoes:
            raise HTTPException(status_code=404, detail="Nenhuma movimentação encontrada para este produto")

        return movimentacoes
    except sqlite3.IntegrityError as e:
        # Caso haja erro de integridade (ex: chave única duplicada)
        raise ValueError("Erro de integridade no banco de dados: " + str(e))
    except sqlite3.OperationalError as e:
        # Erro operacional, como erro de SQL ou banco de dados não encontrado
        raise sqlite3.DatabaseError("Erro operacional no banco de dados: " + str(e))
    except Exception as e:
        # Erros gerais de exceção
        raise Exception("Erro ao processar a solicitação: " + str(e))