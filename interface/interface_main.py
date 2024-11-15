from tkinter import *
import requests  # Importando as funções do backend




# Função para adicionar produto ao ser acionado pela interface
def adicionar_produto_interface():
    nome = nome_entry.get()
    categoria = categoria_entry.get()
    
    try:
        quantidade = int(quantidade_entry.get())
        preco = float(preco_entry.get())
    except ValueError:
        resultado_label.config(text="Quantidade e Preço devem ser números válidos.")
        return
    localizacao = localizacao_entry.get()
    #resultado_label.config(text=f"Produto '{nome}' adicionado com sucesso.")

    if nome and categoria and quantidade is not None and preco is not None and localizacao:
        response = requests.post("http://127.0.0.1:8000/produtos/", json={
            'nome': nome,
            'categoria': categoria,
            'quantidade_estoque': quantidade,
            'preco': preco,
            'localizacao_deposito': localizacao
        }, headers ={ 
            "Content-Type": "application/json"
        })
        if response.status_code == 200:
            resultado_label.config(text=f"Produto '{nome}' adicionado com sucesso.")        
        else:
            resultado_label.config(text=f"Falha ao adicionar Produto: status code '{response.status_code}' ")
    else:
        resultado_label.config(text=f"dados informados inválidos")

# Configuração da interface com Tkinter
janela = Tk()
janela.title("Sistema de Estoque")

# Campos de entrada para o produto
Label(janela, text="Nome do Produto").grid(row=0, column=0)
nome_entry = Entry(janela)
nome_entry.grid(row=0, column=1)

Label(janela, text="Categoria").grid(row=1, column=0)
categoria_entry = Entry(janela)
categoria_entry.grid(row=1, column=1)

Label(janela, text="Quantidade").grid(row=2, column=0)
quantidade_entry = Entry(janela)
quantidade_entry.grid(row=2, column=1)

Label(janela, text="Preço").grid(row=3, column=0)
preco_entry = Entry(janela)
preco_entry.grid(row=3, column=1)

Label(janela, text="Localização").grid(row=4, column=0)
localizacao_entry = Entry(janela)
localizacao_entry.grid(row=4, column=1)

# Botão para adicionar produto
Button(janela, text="Adicionar Produto", command=adicionar_produto_interface).grid(row=5, column=0, columnspan=2)
Button(janela, text="Atualizar Produto", command=atualizar_produto).grid(row=5, column=1, columnspan=2)
Button(janela, text="Sair", command=janela.quit).grid(row=5, column=2)

# Label para mostrar resultados
resultado_label = Label(janela, text="")
resultado_label.grid(row=6, column=0, columnspan=2)

janela.mainloop()