from fastapi import APIRouter, status
import sqlite3
from service.relatorio.gerar_relatorio_service import gerar_relatorio_service
from utils.error.retorna_erro_http import retorna_erro_http

routes = APIRouter()

#End points
#-----------------------------------------------------------------------------------------------------------------

#Gerar relatorio
@routes.get("/relatorio/{id}")
async def gerar_relatorio(id: str):
    try:
        relatorio = gerar_relatorio_service(id)
        return {
            "produto": relatorio["produto"]["nome"],
            "movimentacoes": relatorio["movimentacoes"]
         }
    except ValueError as e:
        retorna_erro_http(str(e),status.HTTP_400_BAD_REQUEST)
    except sqlite3.DatabaseError as e:
        retorna_erro_http(str(e),status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
       retorna_erro_http(str(e),status.HTTP_500_INTERNAL_SERVER_ERROR)