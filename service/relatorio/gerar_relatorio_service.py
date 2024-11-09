import sqlite3
from fastapi import status
from db.queries.queries import conectar
from utils.error.retorna_erro_http import retorna_erro_http

def gerar_relatorio_service(id: str):
    try:

        conexao = conectar()
        cursor = conexao.cursor()

        # Consultando as movimentações do produto
        cursor.execute('''SELECT * FROM movimentacoes WHERE id = ? ORDER BY data_movimentacao DESC''',(id))
        movimentacoes = cursor.fetchall()

        if not movimentacoes:
            retorna_erro_http("Nenhuma movimentação encontrada para este produto", status.HTTP_404_NOT_FOUND)

        # Convertendo as movimentações para uma lista de dicionários
        colunas_movimentacoes = [col[0] for col in cursor.description]
        movimentacoes_dict = [dict(zip(colunas_movimentacoes, mov)) for mov in movimentacoes]


        cursor.execute('''SELECT * FROM produtos WHERE id = ?''',(id))
        produto = cursor.fetchone()

        if not produto:
            retorna_erro_http("Produto não encontrado.",status.HTTP_404_NOT_FOUND)

         # Convertendo o produto para um dicionário
        colunas_produto = [col[0] for col in cursor.description]
        produto_dict = dict(zip(colunas_produto, produto))


        conexao.close()

        return {"produto":produto_dict, "movimentacoes":movimentacoes_dict}
    except sqlite3.IntegrityError as e:
        # Caso haja erro de integridade (ex: chave única duplicada)
        raise ValueError("Erro de integridade no banco de dados: " + str(e))
    except sqlite3.OperationalError as e:
        # Erro operacional, como erro de SQL ou banco de dados não encontrado
        raise sqlite3.DatabaseError("Erro operacional no banco de dados: " + str(e))
    except Exception as e:
        # Erros gerais de exceção
        raise Exception("Erro ao processar a solicitação: " + str(e))