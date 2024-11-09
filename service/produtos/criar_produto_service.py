import sqlite3
from fastapi import status
from schema.schemas import Produto
from db.queries.queries import conectar
from utils.error.retorna_erro_http import retorna_erro_http

def criar_produto_service(produto: Produto):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Validação adicional de dados
        if not produto.nome or not produto.categoria or produto.quantidade_estoque < 0 or produto.preco < 0:
            retorna_erro_http("Dados inválidos: ", status.HTTP_404_NOT_FOUND)

        # Inserção do produto
        cursor.execute('''
            INSERT INTO produtos (nome, categoria, quantidade_estoque, preco, localizacao_deposito)
                VALUES (?, ?, ?, ?, ?)
        ''', (produto.nome, produto.categoria, produto.quantidade_estoque, produto.preco, produto.localizacao_deposito))

        # Registrando a movimentação (entrada)
        cursor.execute('''
        INSERT INTO movimentacoes (nome_produto, quantidade, preco, tipo_movimentacao)
         VALUES (?, ?, ?, ?)
        ''', (produto.nome, produto.quantidade_estoque, produto.preco, 'entrada'))

        conexao.commit()
        conexao.close()
    except sqlite3.IntegrityError as e:
        raise ValueError("Erro de integridade no banco de dados: " + str(e))
    except sqlite3.OperationalError as e:
        raise sqlite3.DatabaseError("Erro operacional no banco de dados: " + str(e))
    except Exception as e:
        raise Exception("Erro ao processar a solicitação: " + str(e))
