from flask import request,g, json, jsonify
from functools import wraps
import secrets
import base64
import time
import hmac
import hashlib
from database.models.idempontecy.idempotency_key import conectar as conectar_idempotency
from database.models.token.token import conectar as conectar_token
cursor_idempotency = conectar_idempotency.cursor()
cursor_token = conectar_token.cursor()

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
            header_64, payload_64, assinatura_64 = token.split(".")
            texto = header_64 + "." + payload_64
            nova_assinatura = hmac.new("Chave secreta".encode(), texto.encode(), hashlib.sha256).digest()
            nova_assinatura_64 = base64.b64encode(nova_assinatura).decode()
            if nova_assinatura_64 == assinatura_64:
                agora = time.time()
                payload_64 = base64.b64decode(payload_64).decode()
                payload = json.loads(payload_64)
                if payload['exp'] <agora:
                    return Controllers.Error(("Token expirado", 401))
                g.cpf = payload['cpf']
                return func(*args, **kwargs)
            return Controllers.Error(("Token invalido"), 401)
        return wrapper

            # cursor_token.execute("SELECT cpf, data_criacao FROM tokens WHERE token = ?", (token,))
            # checar_token = cursor_token.fetchone()
            # if checar_token is None:
            #     return Controllers.Error(("Token invalido"), 401)
            # timestampAgora = time.time()
            # checar_expiracao = timestampAgora - checar_token[1]
            # if checar_expiracao >= 3600:
            #     return Controllers.Error(("Token expirado"), 401)
            # g.cpf = checar_token[0]

    
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
        header_json = json.dumps({"alg" : "HS256", "typ" : "JWT"})
        payload_json = json.dumps({"cpf" : cpf, "exp" : agora + 3600})
        header_bytes = header_json.encode()
        payload_bytes = payload_json.encode()
        header_64 = base64.b64encode(header_bytes).decode()
        payload_64 = base64.b64encode(payload_bytes).decode()
        assinatura = header_64 + "." + payload_64
        token_gerado = hmac.new("Chave secreta".encode(), assinatura.encode(), hashlib.sha256).digest()
        token_gerado = base64.b64encode(token_gerado).decode()
        token = header_64 + "." + payload_64 + "." + token_gerado


        # token = secrets.token_hex(32)
        # cursor_token.execute("INSERT INTO tokens (token, cpf, data_criacao) VALUES (?,?,?)", (token, cpf, agora))
        # conectar_token.commit()
        # return token