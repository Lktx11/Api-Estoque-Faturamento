from flask import request, g
from app import app
from services.usuarios import Usuarios
from services.produtos import Produtos
from services.controllers import Controllers
from services.vendas import Vendas

#usuarios
@app.route("/registrar", methods=['POST'])

def postUsuario():
    dados = request.get_json()
    registrar = Usuarios.Registrar(dados)
    return registrar

@app.route("/login", methods=['POST'])
def postLogin():
    dados = request.get_json()
    login = Usuarios.Login(dados)
    return login
#produtos
@app.route("/produtos/cadastrar", methods=['POST'])
@Controllers.token_required
def postProduto():
    dados = request.get_json()
    registroProduto = Produtos.CriarProduto(dados)
    return registroProduto

@app.route("/produtos", methods=['GET'])
@Controllers.token_required
def getProdutos():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    produtos = Produtos.VerProdutos(page, limit)
    return produtos

@app.route("/produtos", methods=['PUT'])
@Controllers.token_required
def putProduto():
    dados = request.get_json()
    editarProduto = Produtos.EditarProduto(dados)
    return editarProduto

@app.route("/produtos", methods=['DELETE'])
@Controllers.token_required
def deleteProduto():
    dados = request.get_json()
    deletarProduto = Produtos.DeletarProduto(dados)
    return deletarProduto
#vendas
@app.route("/vendas", methods=['POST'])
@Controllers.token_required
@Controllers.idempotency_key
def postVenda():
    dados = request.get_json()
    cpf = g.cpf
    realizarVenda = Vendas.RealizarVenda(dados, cpf)
    return realizarVenda

@app.route("/vendas/faturamento", methods=['GET'])
@Controllers.token_required
def getFaturamento():
    verFaturamento = Vendas.VerFaturamento()
    return verFaturamento


@app.route("/vendas", methods=['GET'])
@Controllers.token_required
def getVendas():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    verVendas = Vendas.VerVendas(page, limit)
    return verVendas


