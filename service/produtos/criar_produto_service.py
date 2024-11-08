import sqlite3
from model.model import Produto
from db.queries.queries import conectar

def criar_produto_service(produto: Produto):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Validação adicional de dados
        if not produto.nome or not produto.categoria or produto.quantidade_estoque < 0 or produto.preco < 0:
            raise ValueError("Dados inválidos para o produto")

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
         # Caso haja erro de integridade (ex: chave única duplicada)
        print("Erro de integridade:", e)  # Adicionando logging
        raise ValueError("Erro de integridade no banco de dados: " + str(e))
    except sqlite3.OperationalError as e:
    # Erro operacional, como erro de SQL ou banco de dados não encontrado
        print("Erro operacional:", e)  # Adicionando logging
        raise sqlite3.DatabaseError("Erro operacional no banco de dados: " + str(e))
    except Exception as e:
        # Erros gerais de exceção
        print("Erro geral:", e)  # Adicionando logging
        raise Exception("Erro ao processar a solicitação: " + str(e))
