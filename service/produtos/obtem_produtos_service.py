import sqlite3
from db.queries.queries import conectar

def obtem_produtos_service():
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT nome, categoria, quantidade_estoque, preco, localizacao_deposito FROM produtos")
        produtos = cursor.fetchall()
        conexao.close()
        return produtos
    except sqlite3.IntegrityError as e:
        # Caso haja erro de integridade (ex: chave única duplicada)
        raise ValueError("Erro de integridade no banco de dados: " + str(e))
    except sqlite3.OperationalError as e:
        # Erro operacional, como erro de SQL ou banco de dados não encontrado
        raise sqlite3.DatabaseError("Erro operacional no banco de dados: " + str(e))
    except Exception as e:
        # Erros gerais de exceção
        raise Exception("Erro ao processar a solicitação: " + str(e))