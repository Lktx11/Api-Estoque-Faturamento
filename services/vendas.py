from services.controllers import Controllers
from flask import jsonify
from database.models.vendas.vendas import conectar as vendas
from database.models.produtos.produtos import conectar as produtos

cursorVendas = vendas.cursor()
cursorProdutos = produtos.cursor()

class Vendas:
    
    def RealizarVenda(dados,cpf):
        if not dados:
            return Controllers.Error(("JSON nao enviado"), 400)
        if 'produto' not in dados:
            return Controllers.Error(("Produto nao enviado"), 400)
        if 'quantidade' not in dados:
            return Controllers.Error(("Quantidade nao enviada"), 400)
        cursorProdutos.execute("SELECT id FROM produtos WHERE produto = ?", (dados['produto'],))
        checarProduto = cursorProdutos.fetchone()
        if checarProduto is None:
            return Controllers.Error(("Esse produto nao existe!"), 404)
        cursorProdutos.execute("SELECT estoque FROM produtos WHERE produto = ? ", (dados["produto"],))
        estoque = cursorProdutos.fetchone()
        if estoque[0] < dados['quantidade']:
            return Controllers.Error(("Você não pode vender acima da quantidade que possui"), 400)
        novoEstoque = estoque[0] - dados['quantidade']
        cursorProdutos.execute("UPDATE produtos SET estoque = ? WHERE produto = ? ", (novoEstoque, dados['produto']))        
        cursorProdutos.execute("SELECT preco_venda FROM produtos WHERE produto = ?", (dados['produto'],))
        valorVenda = cursorProdutos.fetchone()
        total = valorVenda[0] * dados['quantidade']
        cursorVendas.execute("INSERT INTO vendas (usuario_venda, produto, quantidade,total_venda) VALUES (?,?,?,?)", (cpf, dados['produto'], dados['quantidade'], total))
        produtos.commit()
        vendas.commit()
        return jsonify({
            "status" : "sucesso",
            "mensagem" : "Venda registrada!"
        })
        