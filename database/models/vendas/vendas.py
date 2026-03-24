import sqlite3

conectar = sqlite3.connect("database/models/vendas/vendas.db")
cursor = conectar.cursor()

def CriarVendasDB():
    cursor.execute("""CREATE TABLE IF NOT EXISTS vendas(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER NOT NULL,
                id_venda INTEGER NOT NULL,
                total_venda INTEGER
                )""")
    
    conectar.commit()