from flask import request, g
from app import app
from services.usuarios import Usuarios
from services.produtos import Produtos
from services.controllers import Controllers

#usuarios
@app.route("/registrar", methods=['POST'])
@Controllers.token_required
def Registrar():
    dados = request.get_json()
    registrar = Usuarios.Registrar(dados)
    return registrar

@app.route("/login", methods=['POST'])
def Login():
    dados = request.get_json()
    login = Usuarios.Login(dados)
    return login
#produtos


@app.route("/produtos/cadastrar", methods=['POST'])
def CriarProduto():
    dados = request.get_json()
    registroProduto = Produtos.CriarProduto(dados)
    return registroProduto

@app.route("/produtos", methods=['GET'])
def verProdutos():
    produtos = Produtos.VerProdutos()
    return produtos





#vendas