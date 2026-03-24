from flask import request, g
from app import app
from services.usuarios import Usuarios

#usuarios
@app.route("/registrar", methods=['POST'])
def Registrar():
    dados = request.get_json()
    registrar = Usuarios.Registrar(dados)
    return registrar


#produtos

#vendas