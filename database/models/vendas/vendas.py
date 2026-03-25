import sqlite3

conectar = sqlite3.connect("database/models/vendas/vendas.db", check_same_thread=False)
cursor = conectar.cursor()

def CriarVendasDB():
    cursor.execute("""CREATE TABLE IF NOT EXISTS vendas(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                usuario_venda INTEGER NOT NULL,  
                produto TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                total_venda INTEGER
                )""")
    
    conectar.commit()