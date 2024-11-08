import sqlite3

# Função para conectar ao banco de dados
def conectar():
    return sqlite3.connect("estoque.db")

######  TABELAS ######
def criar_tabela_produtos():
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
            tipo_movimentacao TEXT CHECK(tipo_movimentacao IN ('entrada', 'saida', 'solicitacao')) NOT NULL,
            data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (nome_produto) REFERENCES produtos (nome)
        )
    ''')
    conexao.commit()
    conexao.close()


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

def cria_tabelas():
    criar_tabela_produtos()
    criar_tabela_movimentacoes()
    criar_tabela_notas_fiscais()
    criar_tabela_solicitacoes_compras()