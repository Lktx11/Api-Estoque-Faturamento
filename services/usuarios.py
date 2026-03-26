from flask import jsonify, g
from services.controllers import Controllers, token_ativos
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
            return Controllers.Error(("Senha e necessario"), 400)
        
        cursor.execute("INSERT INTO usuarios(nome, cpf, senha, cargo) VALUES (?,?,?, ?)", (dados['nome'].capitalize(), dados['cpf'], dados['senha']))
        conectar.commit()
        return jsonify({
            "status" : "sucesso",
            "mensagem" : "Usuario criado com sucesso"
        })
    
    def Login(dados):
        if not dados:
            return Controllers.Error(("JSON nao enviado"), 401)
        if "cpf" not in dados:
            return Controllers.Error(("Cpf e necessario"), 400)
        if "senha" not in dados:
            return Controllers.Error(("Senha e necessario"), 400)
        cursor.execute("SELECT senha FROM usuarios WHERE cpf = ?", (dados["cpf"],))
        resultado = cursor.fetchone()
        if resultado is None:
            return Controllers.Error(("Usuario nao encontrado"), 404)
        if dados["senha"] != resultado[0]:
            return Controllers.Error(("Senha incorreta"), 401)
        token = dados["cpf"] + dados["senha"]
        token_ativos[token] = dados['cpf'] 
        return jsonify({
            "status" : "sucesso",
            "mensagem" : "Usuario logado com sucesso",
            "token" : token
        })