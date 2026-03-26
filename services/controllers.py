from flask import request,g, json, jsonify
from functools import wraps
import time
from database.models.idempontecy.idempotency_key import conectar
token_ativos = {}
cursor = conectar.cursor()

class Controllers:

    def Error(mensagem, codigo):
        return{
            "status" : "erro",
            "mensagem" : mensagem,
        }, codigo
        


    def token_required(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")
            token = token.replace("Bearer ", "")
            if token is None:
                return Controllers.error(("Token nao enviado"), 400)
            if token not in token_ativos:
                return Controllers.Error(("Token invalido"), 401)
            g.cpf = token_ativos[token]

            return func(*args, **kwargs)


        return wrapper
    
    
    def idempotency_key(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            idempotency = request.headers.get("Idempotency_Key")
            if idempotency is None:
                return func(*args, **kwargs)   
            cursor.execute("SELECT id FROM idempotency WHERE idempotency_key = ?", (idempotency,))
            resultado = cursor.fetchone()
            if resultado is None:
                agora = time.time()         
                metodo = request.method
                rota = request.path
                resposta = func(*args,**kwargs)
                status_code = resposta[1]
                cursor.execute("INSERT INTO idempotency (idempotency_key, rota, metodo, status_code, resposta, data_criacao) VALUES (?,?,?,?,?,?)", (idempotency, rota, metodo, status_code, json.dumps(resposta[0].json), agora))
                return resposta
            cursor.execute("SELECT status_code, resposta FROM idempotency WHERE idempotency_key = ?", (idempotency,))
            resposta = cursor.fetchone()
            dados = json.loads(resposta[1])
            return jsonify(dados), resposta[0]
        
        return wrapper