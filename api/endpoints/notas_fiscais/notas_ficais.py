from fastapi import APIRouter, status
import sqlite3
from schema.schemas import NotaFiscal
from service.notas_fiscais.cadastrar_nota_fiscal_service import cadastrar_nota_fiscal_service
from utils.error.retorna_erro_http import retorna_erro_http

routes = APIRouter()

#End points
#-----------------------------------------------------------------------------------------------------------------

# Cadastrar Nota Fiscal
@routes.post("/notas_fiscais/")
async def cadastrar_nota_fiscal(nota: NotaFiscal):
    try:
        cadastrar_nota_fiscal_service(nota)
        return {"message": "Nota fiscal cadastrada com sucesso"}
    except ValueError as e:
        retorna_erro_http(str(e),status.HTTP_400_BAD_REQUEST)
    except sqlite3.DatabaseError as e:
        retorna_erro_http(str(e),status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
       retorna_erro_http(str(e),status.HTTP_500_INTERNAL_SERVER_ERROR)