from fastapi import FastAPI, status
import sqlite3
from model.model import Produto, NotaFiscal, SolicitacaoCompra
from service.produtos import criar_produto_service, obtem_produtos_service, alterar_produto_service, deletar_produto_service
from service.relatorio import gerar_relatorio_service
from service.notas_fiscais import cadastrar_nota_fiscal_service
from service.solicitacoes.compra import solicitar_compra_service
from db.queries.queries import cria_tabelas
from error import retorna_erro_http


# Configuração do FastAPI
app = FastAPI()

# Cria as tabelas de no banco
cria_tabelas()

#End points
#-----------------------------------------------------------------------------------------------------------------

#Raiz
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Criar um produto (Create)
@app.post("/produtos")
def criar_produto(produto: Produto):
    try:
        criar_produto_service(produto)
        return {"message": "Produto adicionado com sucesso"}
    except ValueError as e:
        retorna_erro_http("Erro ao criar produto: " + str(e),status.HTTP_400_BAD_REQUEST)
    except sqlite3.DatabaseError as e:
        retorna_erro_http("Erro ao criar produto: banco de dados: " + str(e),status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
       retorna_erro_http("Erro ao criar produto: inesperado: " + str(e),status.HTTP_500_INTERNAL_SERVER_ERROR)

# Listar todos os produtos (Read)
@app.get("/produtos/")
def listar_produtos():
    try:
        produtos = obtem_produtos_service()
        if not produtos:
            retorna_erro_http("Nenhum produto encontrado", status.HTTP_404_NOT_FOUND)
        return {"produtos": produtos}
    except ValueError as e:
        retorna_erro_http("Erro ao listar produtos: " + str(e),status.HTTP_400_BAD_REQUEST)
    except sqlite3.DatabaseError as e:
        retorna_erro_http("Erro ao listar produtos: banco de dados: " + str(e),status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
       retorna_erro_http("Erro ao listar produtos: inesperado: " + str(e),status.HTTP_500_INTERNAL_SERVER_ERROR)


# Atualizar produtos
@app.put("/produtos/")
def atualizar_produto(nome: str, produto: Produto):
    try:
        alterar_produto_service(nome, produto)
        return {"message": "Produto atualizado com sucesso"}
    except ValueError as e:
        retorna_erro_http("Erro ao atualizar produto: " + str(e),status.HTTP_400_BAD_REQUEST)
    except sqlite3.DatabaseError as e:
        retorna_erro_http("Erro ao atualizar produto: banco de dados: " + str(e),status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
       retorna_erro_http("Erro ao atualizar produto: inesperado: " + str(e),status.HTTP_500_INTERNAL_SERVER_ERROR)


# Deletar um produto por NOME (Delete)
@app.delete("/produtos/{nome}")
def deletar_produto(nome: str):
    try:
        deletar_produto_service(nome)
        return {"message": "Produto deletado com sucesso"}
    except ValueError as e:
        retorna_erro_http("Erro ao deletar produto: " + str(e),status.HTTP_400_BAD_REQUEST)
    except sqlite3.DatabaseError as e:
        retorna_erro_http("Erro ao deletar produto: banco de dados: " + str(e),status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
       retorna_erro_http("Erro ao deletar produto: inesperado: " + str(e),status.HTTP_500_INTERNAL_SERVER_ERROR)

#Gerar relatorio
@app.get("/relatorio/{nome}")
def gerar_relatorio(nome: str):
    try:
        movimentacoes = gerar_relatorio_service(nome)
        return {
            "produto": nome,
            "movimentacoes": [
                {
                    "data": m[5],
                    "quantidade": m[2],
                    "preco": m[3],
                    "tipo": m[4]
                }
                    for m in movimentacoes
                ]
         }
    except ValueError as e:
        retorna_erro_http("Erro ao gerar relatório: " + str(e),status.HTTP_400_BAD_REQUEST)
    except sqlite3.DatabaseError as e:
        retorna_erro_http("Erro ao gerar relatório: banco de dados: " + str(e),status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
       retorna_erro_http("Erro ao gerar relatório: inesperado: " + str(e),status.HTTP_500_INTERNAL_SERVER_ERROR)

# Cadastrar Nota Fiscal
@app.post("/notas_fiscais/")
def cadastrar_nota_fiscal(nota: NotaFiscal):
    try:
        cadastrar_nota_fiscal_service(nota)
        return {"message": "Nota fiscal cadastrada com sucesso"}
    except ValueError as e:
        retorna_erro_http("Erro ao criar nota fiscal: " + str(e),status.HTTP_400_BAD_REQUEST)
    except sqlite3.DatabaseError as e:
        retorna_erro_http("Erro ao criar nota fiscal: banco de dados: " + str(e),status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
       retorna_erro_http("Erro ao criar nota fiscal: inesperado: " + str(e),status.HTTP_500_INTERNAL_SERVER_ERROR)

# Solicitar Compra
@app.post("/solicitacoes_compras/")
def solicitar_compra(solicitacao: SolicitacaoCompra):
    try:
        solicitar_compra_service(solicitacao)
        return {"message": "Solicitação de compra registrada com sucesso"}
    except ValueError as e:
        retorna_erro_http("Erro ao solicitar compra: " + str(e),status.HTTP_400_BAD_REQUEST)
    except sqlite3.DatabaseError as e:
        retorna_erro_http("Erro ao solicitar compra: banco de dados: " + str(e),status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
       retorna_erro_http("Erro ao solicitar compra: inesperado: " + str(e),status.HTTP_500_INTERNAL_SERVER_ERROR)

