from flask import jsonify, g
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
            return Controllers.Error(("Senha e necessario"), 400)
        cursor.execute("SELECT id FROM usuarios WHERE cpf = ?", (dados['cpf'],))
        checar_cpf_existe = cursor.fetchone()
        if checar_cpf_existe is not None:
            return Controllers.Error(("Esse cpf ja esta registrado!"), 400)
        cursor.execute("INSERT INTO usuarios(nome, cpf, senha) VALUES (?,?,?)", (dados['nome'], dados['cpf'], dados['senha']))
        conectar.commit()
        return jsonify({
            "status" : "sucesso",
            "mensagem" : "Usuario criado com sucesso"
        }), 201
    
    def Login(dados):
        if not dados:
            return Controllers.Error(("JSON nao enviado"), 400)
        if "cpf" not in dados:
            return Controllers.Error(("Cpf e necessario"), 400)
        if "senha" not in dados:
            return Controllers.Error(("Senha e necessario"), 400)
        cursor.execute("SELECT senha FROM usuarios WHERE cpf = ?", (dados["cpf"],))
        resultado_senha = cursor.fetchone()
        if resultado_senha is None:
            return Controllers.Error(("Usuario nao encontrado"), 404)
        if dados["senha"] != resultado_senha[0]: #0 = Senha
            return Controllers.Error(("Senha incorreta"), 401)
        token_usuario = Controllers.gerar_token(dados['cpf'])
        return jsonify({
            "status" : "sucesso",
            "mensagem" : "Usuario logado com sucesso",
            "token" : token_usuario
        }), 200