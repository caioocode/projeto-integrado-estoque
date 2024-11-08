import sqlite3
from model.model import NotaFiscal
from db.queries.queries import conectar

def cadastrar_nota_fiscal_service(nota: NotaFiscal):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Calcular o valor total (se necessário)
        if nota.valor_total is None:
            nota.valor_total = nota.quantidade * nota.preco

        # Inserir a nova nota fiscal
        cursor.execute('''INSERT INTO notas_fiscais (numero, nome_produto, quantidade, preco, valor_total, tipo_movimentacao)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (nota.numero, nota.nome_produto, nota.quantidade, nota.preco, nota.valor_total, nota.tipo_movimentacao))

        # Registrar a movimentação
        cursor.execute('''INSERT INTO movimentacoes (nome_produto, quantidade, preco, tipo_movimentacao)
        VALUES (?, ?, ?, ?)''',
        (nota.nome_produto, nota.quantidade, nota.preco, nota.tipo_movimentacao))

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