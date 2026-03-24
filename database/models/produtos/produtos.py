import sqlite3

conectar = sqlite3.connect("database/models/produtos/produtos.db")
cursor = conectar.cursor()

def CriarProdutosDB():
    cursor.execute("""CREATE TABLE IF NOT EXISTS produtos(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                produto TEXT NOT NULL,
                preco INTEGER NOT NULL,
                estoque INTEGER NOT NULL
                )""")
    
    conectar.commit()