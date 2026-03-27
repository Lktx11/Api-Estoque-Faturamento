from services.controllers import Controllers
from flask import jsonify, g
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
        checar_produto_existente = cursorProdutos.fetchone()
        if checar_produto_existente is None:
            return Controllers.Error(("Esse produto nao existe!"), 404)
        cursorProdutos.execute("SELECT estoque FROM produtos WHERE produto = ? ", (dados["produto"],))
        estoque_produto = cursorProdutos.fetchone()
        if estoque_produto[0] < dados['quantidade']: # 0 = Quantidade que possui de estoque
            return Controllers.Error(("Você não pode vender acima da quantidade que possui"), 400)
        novo_estoque = estoque_produto[0] - dados['quantidade']
        cursorProdutos.execute("UPDATE produtos SET estoque = ? WHERE produto = ? ", (novo_estoque, dados['produto']))        
        cursorProdutos.execute("SELECT preco_venda FROM produtos WHERE produto = ?", (dados['produto'],))
        valor_venda_produto = cursorProdutos.fetchone()
        total = valor_venda_produto[0] * dados['quantidade'] #0 = Valor de venda do produto
        cursorVendas.execute("INSERT INTO vendas (usuario_venda, produto, quantidade,total_venda) VALUES (?,?,?,?)", (cpf, dados['produto'], dados['quantidade'], total))
        produtos.commit()
        vendas.commit()
        return jsonify({
            "status" : "sucesso",
            "mensagem" : "Venda registrada!",
        }), 200
        


    def VerFaturamento():
        cursorVendas.execute("SELECT total_venda FROM vendas")
        total_vendas = cursorVendas.fetchall()
        vendaTotais = sum(preco[0] for preco in total_vendas)
        cursorVendas.execute("SELECT produto, quantidade FROM vendas")
        produto_quantidade = cursorVendas.fetchall()
        gastoTotais = 0
        for produto, quantidade in produto_quantidade:
            cursorProdutos.execute("SELECT preco_compra FROM produtos WHERE produto = ?", (produto,))
            preco_compra = cursorProdutos.fetchone()[0]
            gastoTotais += quantidade * preco_compra
        faturamento = vendaTotais - gastoTotais
        return jsonify({
            "status" : "sucesso",
            "faturamento" : faturamento 
        })
        
    def VerVendas(page, limit):
        offset = (page - 1) * limit
        cursorVendas.execute("SELECT usuario, produto, total_venda, quantidade FROM vendas LIMIT ? OFFSET ?", (limit, offset))
        registro_vendas     = cursorVendas.fetchall()
        vendas = {}
        for venda in registro_vendas:
            usuario, produto, total_venda, quantidade = venda 
            vendas[produto] = {
                "Vendido por" : usuario,
                "Quantidade" : quantidade,
                "Valor total da venda" : total_venda,
            }
        cursorVendas.execute("SELECT COUNT (*) FROM vendas")
        quantidade_vendas = cursorVendas.fetchone()
        total_pages = quantidade_vendas[0] / limit
        return jsonify({
            "status" : "sucesso",
            "page" : page,
            "limit" : limit,
            "total_page" : total_pages,
            "dados" : vendas
        }), 200
        
        
        