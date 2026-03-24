from flask import request,g
from functools import wraps
token_ativos = {}


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
            g.cpfToken = token_ativos[token]

            return func(*args, **kwargs)


        return wrapper