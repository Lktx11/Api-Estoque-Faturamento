import sqlite3

conectar = sqlite3.connect("database/models/usuarios/usuarios.db")

cursor = conectar.cursor()


def CriarUsuariosDB():
    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
                )""")
    
    conectar.commit()