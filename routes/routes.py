from flask import request, g
from app import app
from services.usuarios import Usuarios
from services.produtos import Produtos
from services.controllers import Controllers
from services.vendas import Vendas

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
@Controllers.token_required
def criarProduto():
    dados = request.get_json()
    registroProduto = Produtos.CriarProduto(dados)
    return registroProduto

@app.route("/produtos", methods=['GET'])
@Controllers.token_required
def verProdutos():
    produtos = Produtos.VerProdutos()
    return produtos

@app.route("/produtos", methods=['PUT'])
@Controllers.token_required
def editarProduto():
    dados = request.get_json()
    editarProduto = Produtos.EditarProduto(dados)
    return editarProduto

@app.route("/produtos", methods=['DELETE'])
@Controllers.token_required
def deletarProduto():
    dados = request.get_json()
    deletarProduto = Produtos.DeletarProduto(dados)
    return deletarProduto


#vendas



@app.route("/vendas", methods=['POST'])
@Controllers.token_required
def realizarVenda():
    dados = request.get_json()
    cpf = g.cpf
    realizarVenda = Vendas.RealizarVenda(dados, cpf)
    return realizarVenda

@app.route("/vendas/faturamento", methods=['GET'])
def verFaturamento():
    verFaturamento = Vendas.VerFaturamento()
    return verFaturamento