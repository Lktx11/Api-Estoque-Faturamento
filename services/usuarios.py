from flask import Flask, jsonify, g
from services.controllers import Controllers
from database.models.usuarios.usuarios import conectar
cursor = conectar.cursor()

class Usuarios:

    def Registrar(dados):
        if not dados:
            return Controllers.Error(("JSON nao enviado"), 400)
        if "nome" not in dados:
            return Controllers.Error(("Nome e necessario"), 400)
        if "cpf" not in dados:
            return Controllers.Error(("Cpf e necessario"), 400)
        if "senha" not in dados:
            return Controllers.Error(("Nome e necessario"), 400)
        
        cursor.execute("INSERT INTO usuarios(nome, cpf, senha, cargo) VALUES (?,?,?, ?)", (dados['nome'].capitalize(), dados['cpf'], dados['senha'], "Contratado"))
        conectar.commit()
        return jsonify({
            "status" : "sucesso",
            "mensagem" : "Usuario criado com sucesso"
        })