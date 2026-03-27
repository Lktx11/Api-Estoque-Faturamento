import sqlite3

conectar = sqlite3.connect("database/models/token/token.db", check_same_thread=False)
cursor = conectar.cursor()

def CriarTokenDB():  
    cursor.execute("""CREATE TABLE IF NOT EXISTS tokens(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                token TEXT NOT NULL,
                cpf TEXT NOT NULL,
                data_criacao INTEGER NOT NULL
                )""")
    
    conectar.commit()