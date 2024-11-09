import sqlite3
from fastapi import status
from schema.schemas import Produto
from db.queries.queries import conectar
from utils.error.retorna_erro_http import retorna_erro_http


def alterar_produto_service(id: str, produto: Produto):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Verificar se o produto existe
        cursor.execute("SELECT quantidade_estoque FROM produtos WHERE id = ?", (id))
        produto_antigo = cursor.fetchone()

        if not produto_antigo:
            retorna_erro_http("Produto não encontrado.",status.HTTP_404_NOT_FOUND)

        # Atualizando produto
        cursor.execute('''UPDATE produtos SET nome = ?, categoria = ?, quantidade_estoque = ?, preco = ?, localizacao_deposito = ?WHERE nome = ?''',
            (produto.nome, produto.categoria, produto.quantidade_estoque, produto.preco, produto.localizacao_deposito, produto.nome))

        # Calculando a diferença de quantidade
        diferenca = produto.quantidade_estoque - produto_antigo[1]
        if diferenca > 0:
            tipo_movimentacao = 'entrada'
        else:
            tipo_movimentacao = 'saida'

        if diferenca != 0:
            # Registrando a movimentação
            cursor.execute('''INSERT INTO movimentacoes (nome_produto, quantidade, preco, tipo_movimentacao)
            VALUES (?, ?, ?, ?)''',
            (produto.nome, abs(diferenca), produto.preco, tipo_movimentacao))
        # Verificar se o produto existe
        cursor.execute("SELECT * from produtos WHERE id = ?", (id))
        produto_alterado = cursor.fetchone()

        conexao.commit()
        conexao.close()

        return produto_alterado
    except sqlite3.IntegrityError as e:
        # Caso haja erro de integridade (ex: chave única duplicada)
        raise ValueError("Erro de integridade no banco de dados: " + str(e))
    except sqlite3.OperationalError as e:
        # Erro operacional, como erro de SQL ou banco de dados não encontrado
        raise sqlite3.DatabaseError("Erro operacional no banco de dados: " + str(e))
    except Exception as e:
        # Erros gerais de exceção
        raise Exception("Erro ao processar a solicitação: " + str(e))
