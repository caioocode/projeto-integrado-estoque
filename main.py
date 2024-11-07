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

# Função para conectar ao banco de dados
def conectar():
    return sqlite3.connect("estoque.db")

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

# Criar um produto (Create)
@app.post("/produtos/")
def adicionar_produto(nome, categoria, quantidade_estoque, preco, localizacao_deposito):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO produtos (nome, categoria, quantidade_estoque, preco, localizacao_deposito)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, categoria, quantidade_estoque, preco, localizacao_deposito))
    conexao.commit()
    conexao.close()
    return {"message": "Produto adicionado com sucesso"}

# Listar todos os produtos (Read)
@app.get("/produtos/")
def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conexao.close()
    for produto in produtos:
        print(produto)

# Atualizar um produto por ID (Update)
@app.put("/produtos/{nome}")
def atualizar_produto(nome, categoria, quantidade_estoque, preco, localizacao_deposito):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('''
        UPDATE produtos
        SET nome = ?, categoria = ?, quantidade_estoque = ?, preco = ?, localizacao_deposito = ?
        WHERE id = ?
    ''', (nome, categoria, quantidade_estoque, preco, localizacao_deposito, id_produto))
    conexao.commit()
    conexao.close()
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return {"message": "Produto atualizado com sucesso"}

# Deletar um produto por ID (Delete)
@app.delete("/produtos/{nome}")
def deletar_produto(nome: str):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
    conexao.commit()
    conexao.close()
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return {"message": "Produto deletado com sucesso"}

