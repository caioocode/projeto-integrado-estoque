from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

# Configuração do FastAPI
app = FastAPI()

# Modelo de Dados para o Produto
class Produto(BaseModel):
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


# Função para conectar ao banco de dados
def conectar():
    return sqlite3.connect("estoque.db")

######  TABELAS ######
def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            quantidade_estoque INTEGER NOT NULL,
            preco REAL NOT NULL,
            localizacao_deposito TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

criar_tabela()


# Criar tabela de movimentações (execute apenas uma vez)
def criar_tabela_movimentacoes():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL,
            tipo_movimentacao TEXT CHECK(tipo_movimentacao IN ('entrada', 'saida')) NOT NULL,
            data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (nome_produto) REFERENCES produtos (nome)
        )
    ''')
    conexao.commit()
    conexao.close()

# Chame a função para criar a tabela de movimentações
criar_tabela_movimentacoes()


# Criar tabela de notas fiscais
def criar_tabela_notas_fiscais():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notas_fiscais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT NOT NULL,
            nome_produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL,
            valor_total REAL NOT NULL,
            tipo_movimentacao TEXT CHECK(tipo_movimentacao IN ('entrada', 'saida')) NOT NULL,
            data_emissao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (nome_produto) REFERENCES produtos (nome)
        )
    ''')
    conexao.commit()
    conexao.close()

criar_tabela_notas_fiscais()


# Criar tabela de solicitações de compras
def criar_tabela_solicitacoes_compras():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitacoes_compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            data_solicitacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (nome_produto) REFERENCES produtos (nome)
        )
    ''')
    conexao.commit()
    conexao.close()

criar_tabela_solicitacoes_compras()

#-----------------------------------------------------------------------------------------------------------------
# Criar um produto (Create)
@app.post("/produtos/")
def adicionar_produto(nome, categoria, quantidade_estoque, preco, localizacao_deposito):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO produtos (nome, categoria, quantidade_estoque, preco, localizacao_deposito)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, categoria, quantidade_estoque, preco, localizacao_deposito))

    # Registrando a movimentação (entrada)
    cursor.execute('''
        INSERT INTO movimentacoes (nome_produto, quantidade, preco, tipo_movimentacao)
        VALUES (?, ?, ?, ?)
    ''', (nome, quantidade_estoque, preco, 'entrada'))

    conexao.commit()
    conexao.close()
    return {"message": "Produto adicionado com sucesso"}


# Listar todos os produtos (Read)
@app.get("/produtos/")
def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, categoria, quantidade_estoque, preco, localizacao_deposito FROM produtos")
    produtos = cursor.fetchall()
    conexao.close()
    
    if not produtos:
        raise HTTPException(status_code=404, detail="Nenhum produto encontrado")

    return {"produtos": produtos}

@app.put("/produtos/")
def atualizar_produto(nome: str, produto: Produto):
    conexao = conectar()
    cursor = conexao.cursor()

    # Verificar se o produto existe
    cursor.execute("SELECT nome, quantidade_estoque FROM produtos WHERE nome = ?", (nome,))
    produto_antigo = cursor.fetchone()

    if produto_antigo is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Atualizando produto
    cursor.execute('''
        UPDATE produtos
        SET nome = ?, categoria = ?, quantidade_estoque = ?, preco = ?, localizacao_deposito = ?
        WHERE nome = ?
    ''', (produto.nome, produto.categoria, produto.quantidade_estoque, produto.preco, produto.localizacao_deposito, nome))
    
    # Calculando a diferença de quantidade
    diferenca = produto.quantidade_estoque - produto_antigo[1]
    tipo_movimentacao = 'entrada' if diferenca > 0 else 'saida'

    if diferenca != 0:
        # Registrando a movimentação
        cursor.execute('''
            INSERT INTO movimentacoes (nome_produto, quantidade, preco, tipo_movimentacao)
            VALUES (?, ?, ?, ?)
        ''', (produto.nome, abs(diferenca), produto.preco, tipo_movimentacao))

    conexao.commit()
    conexao.close()
    
    return {"message": "Produto atualizado com sucesso"}


# Deletar um produto por NOME (Delete)
@app.delete("/produtos/{nome}")
def deletar_produto(nome: str):
    conexao = conectar()
    cursor = conexao.cursor()

    # Pegando o produto para a movimentação de saída
    cursor.execute("SELECT nome, quantidade_estoque FROM produtos WHERE nome = ?", (nome,))
    produto = cursor.fetchone()

    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Deletando o produto
    cursor.execute("DELETE FROM produtos WHERE nome = ?", (nome,))
    
    # Registrando a movimentação de saída após a exclusão
    cursor.execute('''
        INSERT INTO movimentacoes (nome_produto, quantidade, preco, tipo_movimentacao)
        VALUES (?, ?, ?, ?)
    ''', (nome, produto[1], 'saida'))  # produto[1] é a quantidade_estoque

    conexao.commit()
    conexao.close()
    
    return {"message": "Produto deletado com sucesso"}


#Gerar relatorio
@app.get("/produtos/{nome}")
def gerar_relatorio(nome: str):
    conexao = conectar()
    cursor = conexao.cursor()

        # Consultando as movimentações do produto
    cursor.execute('''
        SELECT * FROM movimentacoes WHERE nome_produto = ? ORDER BY data_movimentacao DESC
    ''', (nome,))
    movimentacoes = cursor.fetchall()
    
    conexao.close()

    if not movimentacoes:
        raise HTTPException(status_code=404, detail="Nenhuma movimentação encontrada para este produto")

    # Retornando as movimentações como um relatório
    return {
        "produto": nome,
        "movimentacoes": [{"data": m[5], "quantidade": m[2], "preco": m[3], "tipo": m[4]} for m in movimentacoes]
    }

# Cadastrar Nota Fiscal
@app.post("/notas_fiscais/")
def cadastrar_nota_fiscal(nota: NotaFiscal):
    conexao = conectar()
    cursor = conexao.cursor()
    
    # Calcular o valor total (se necessário)
    if nota.valor_total is None:
        nota.valor_total = nota.quantidade * nota.preco

    # Inserir a nova nota fiscal
    cursor.execute('''
        INSERT INTO notas_fiscais (numero, nome_produto, quantidade, preco, valor_total, tipo_movimentacao)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nota.numero, nota.nome_produto, nota.quantidade, nota.preco, nota.valor_total, nota.tipo_movimentacao))
    
    # Registrar a movimentação
    cursor.execute('''
        INSERT INTO movimentacoes (nome_produto, quantidade, preco, tipo_movimentacao)
        VALUES (?, ?, ?, ?)
    ''', (nota.nome_produto, nota.quantidade, nota.preco, nota.tipo_movimentacao))
    
    conexao.commit()
    conexao.close()
    return {"message": "Nota fiscal cadastrada com sucesso"}

# Solicitar Compra
@app.post("/solicitacoes_compras/")
def solicitar_compra(solicitacao: SolicitacaoCompra):
    conexao = conectar()
    cursor = conexao.cursor()

    # Inserir a nova solicitação de compra
    cursor.execute('''
        INSERT INTO solicitacoes_compras (nome_produto, quantidade)
        VALUES (?, ?)
    ''', (solicitacao.nome_produto, solicitacao.quantidade))

    #Registrar a movimentação
    cursor.execute('''
        INSERT INTO movimentacoes (nome_produto, quantidade, preco, tipo_movimentacao)
        VALUES (?, ?, ?, ?)
    ''', (solicitacao.nome_produto, solicitacao.quantidade, 'saida'))

    conexao.commit()
    conexao.close()
    return {"message": "Solicitação de compra registrada com sucesso"}