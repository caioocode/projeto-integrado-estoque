import sqlite3
from fastapi import HTTPException
from model.model import Produto
from db.queries.queries import conectar


def alterar_produto_service(nome: str, produto: Produto):
    try:

        conexao = conectar()
        cursor = conexao.cursor()

        # Verificar se o produto existe
        cursor.execute("SELECT nome, quantidade_estoque FROM produtos WHERE nome = ?", (nome,))
        produto_antigo = cursor.fetchone()

        if produto_antigo is None:
            raise HTTPException(status_code = 404, detail = "Produto não encontrado")

        # Atualizando produto
        cursor.execute('''UPDATE produtos SET nome = ?, categoria = ?, quantidade_estoque = ?, preco = ?, localizacao_deposito = ?WHERE nome = ?''',
            (produto.nome, produto.categoria, produto.quantidade_estoque, produto.preco, produto.localizacao_deposito, nome))

        # Calculando a diferença de quantidade
        diferenca = produto.quantidade_estoque - produto_antigo[1]
        tipo_movimentacao = 'entrada' if diferenca > 0 else 'saida'

        if diferenca != 0:
            # Registrando a movimentação
            cursor.execute('''INSERT INTO movimentacoes (nome_produto, quantidade, preco, tipo_movimentacao)
            VALUES (?, ?, ?, ?)''',
            (produto.nome, abs(diferenca), produto.preco, tipo_movimentacao))

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
