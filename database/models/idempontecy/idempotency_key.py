import sqlite3

conectar = sqlite3.connect("database/models/idempontecy/idempotency_key.db", check_same_thread=False)
cursor = conectar.cursor()

def CriarIdempotencyDB():
    cursor.execute("""CREATE TABLE IF NOT EXISTS idempotency(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                idempotency_key TEXT NOT NULL,
                rota TEXT NOT NULL,
                metodo TEXT NOT NULL,
                status_code INTEGER NOT NULL,
                resposta TEXT NOT NULL,
                data_criacao INTEGER NOT NULL
                )""")
    
    conectar.commit()
    
    