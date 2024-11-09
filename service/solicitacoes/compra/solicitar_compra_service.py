import sqlite3
from schema.schemas import SolicitacaoCompra
from db.queries.queries import conectar

def solicitar_compra_service(solicitacao: SolicitacaoCompra):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Inserir a nova solicitação de compra
        cursor.execute('''INSERT INTO solicitacoes_compras (nome_produto, quantidade)
        VALUES (?, ?)''',
        (solicitacao.nome_produto, solicitacao.quantidade))

        # Registrar a movimentação com o preço incluído
        cursor.execute('''INSERT INTO movimentacoes (nome_produto, quantidade, preco, tipo_movimentacao)
        VALUES (?, ?, ?, ?)''',
        (solicitacao.nome_produto, solicitacao.quantidade, solicitacao.preco, 'entrada'))

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