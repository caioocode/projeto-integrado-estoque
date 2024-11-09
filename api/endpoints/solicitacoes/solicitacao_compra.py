from fastapi import APIRouter, status
import sqlite3
from schema.schemas import SolicitacaoCompra
from service.solicitacoes.compra.solicitar_compra_service import solicitar_compra_service
from utils.error.retorna_erro_http import retorna_erro_http

routes = APIRouter()

#End points
#-----------------------------------------------------------------------------------------------------------------

# Solicitar Compra
@routes.post("/solicitacoes_compras/")
def solicitar_compra(solicitacao: SolicitacaoCompra):
    try:
        solicitar_compra_service(solicitacao)
        return {"message": "Solicitação de compra registrada com sucesso"}
    except ValueError as e:
        retorna_erro_http(str(e),status.HTTP_400_BAD_REQUEST)
    except sqlite3.DatabaseError as e:
        retorna_erro_http(str(e),status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
       retorna_erro_http(str(e),status.HTTP_500_INTERNAL_SERVER_ERROR)