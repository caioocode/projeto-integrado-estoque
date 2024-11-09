from pydantic import BaseModel

# Modelo de Dados para o Produto
class Produto(BaseModel):
    nome: str
    categoria: str
    quantidade_estoque: int
    preco: float
    localizacao_deposito: str

class ProdutoResponse(BaseModel):
    id: int
    nome: str
    categoria: str
    quantidade_estoque: int
    preco: float
    localizacao_deposito: str

# Modelo de Dados para a Movimentação
class Movimentacao(BaseModel):
    nome_produto: str
    quantidade: int
    preco: float
    tipo_movimentacao: str

# Modelo de Dados para a Nota Fiscal
class NotaFiscal(BaseModel):
    numero: str
    nome_produto: str
    quantidade: int
    preco: float
    valor_total: float
    tipo_movimentacao: str  # entrada ou saída

#Modelo de Dados para Solicitação de Compras
class SolicitacaoCompra(BaseModel):
    nome_produto: str
    quantidade: int
    preco: float
