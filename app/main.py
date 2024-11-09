from fastapi import FastAPI
from api.endpoints.produtos.produtos import routes as produtos
from api.endpoints.relatorios.relatorios import routes as relatorios
from api.endpoints.notas_fiscais.notas_ficais import routes as notas_ficais
from api.endpoints.solicitacoes.solicitacao_compra import routes as solicitacao_compra
from db.queries.queries import cria_tabelas

# Configuração do FastAPI
app = FastAPI()

# Cria as tabelas de no banco
cria_tabelas()

# Inclui rotas
app.include_router(produtos, prefix="/v1", tags=["Produtos"])
app.include_router(relatorios, prefix="/v1", tags=["Relatórios"])
app.include_router(notas_ficais, prefix="/v1", tags=["Notas fiscais"])
app.include_router(solicitacao_compra, prefix="/v1", tags=["Solicitações de compra"])





