from flask import request,g, json, jsonify
from functools import wraps
import jwt
import time
from database.models.idempontecy.idempotency_key import conectar as conectar_idempotency
from database.models.usuarios.usuarios import conectar as conectar_usuarios
cursor_usuarios = conectar_usuarios.cursor()
cursor_idempotency = conectar_idempotency.cursor()
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
            if token is None:
                return Controllers.error(("Token nao enviado"), 400)
            token = token.replace("Bearer ", "")
            try:
                payload = jwt.decode(token, "Chave secreta", algorithms=["HS256"])
                g.cpf = payload['cpf']
                return func(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return Controllers.Error(("Token expirado"), 401)
            except jwt.InvalidTokenError:
                return Controllers.Error(("Token invalido"), 401)
        return wrapper

    def idempotency_key(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            idempotency = request.headers.get("Idempotency-Key")
            if idempotency is None:
                return func(*args, **kwargs)   
            cursor_idempotency.execute("SELECT id FROM idempotency WHERE idempotency_key = ?", (idempotency,))
            resultado = cursor_idempotency.fetchone()
            if resultado is None:
                agora = time.time()         
                metodo = request.method
                rota = request.path
                resposta = func(*args,**kwargs)
                status_code = resposta[1]
                cursor_idempotency.execute("INSERT INTO idempotency (idempotency_key, rota, metodo, status_code, resposta, data_criacao) VALUES (?,?,?,?,?,?)", (idempotency, rota, metodo, status_code, json.dumps(resposta[0].json), agora))
                conectar_idempotency.commit()
                return resposta
            cursor_idempotency.execute("SELECT status_code, resposta FROM idempotency WHERE idempotency_key = ?", (idempotency,))
            resposta = cursor_idempotency.fetchone()
            dados = json.loads(resposta[1])
            return jsonify(dados), resposta[0]
        
        return wrapper
    
    def gerar_token(cpf):
        agora = time.time()
        payload = {
            "cpf" : cpf, 
            "exp" : agora + 3600
        }
        token = jwt.encode(payload, "Chave Secreta", algorithm="HS256")
        return token
    
    
    def is_admin(func, cpf):
        @wraps(func, cpf )
        def wrapper(*args, **kwargs)
            cursor_usuarios.execute("SELECT cargo FROM usuarios WHERE cpf = ?", (cpf, ))
            cargo_usuario = cursor_usuarios.fetchone()
            if cargo_usuario.lower() != "admin":
                Controllers.Error(("Esse usuario nao é admin!"), 401)
            return func(*args, **kwargs)
        return wrapper