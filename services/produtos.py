from services.controllers import Controllers
from flask import jsonify
from database.models.produtos.produtos import conectar
cursor = conectar.cursor()


class Produtos:
    def CriarProduto(dados):
        if not dados:
            return Controllers.Error(("JSON nao enviado"), 400)
        if "produto" not in dados:
            return Controllers.Error(("Nome do produto e necessario"), 400)
        if "preco_compra" not in dados:
            return Controllers.Error(("Preco de compra e necessario"), 400)
        if "preco_venda" not in dados:
            return Controllers.Error(("Preco de venda e necessario"), 400)
        if "estoque" not in dados:
            return Controllers.Error(("Estoque e necessario"), 400)
        cursor.execute("SELECT estoque FROM produtos WHERE produto = ?", (dados['produto'],))
        checar_estoque_produto = cursor.fetchone()
        if checar_estoque_produto is None:
            cursor.execute("""INSERT INTO produtos (produto, preco_compra, preco_venda, estoque) VALUES (?,?,?,?)
                           """, (dados["produto"], dados["preco_compra"], dados["preco_venda"], dados["estoque"]))
            conectar.commit()
            return jsonify({
                "status" : "sucesso",
                "mensagem" : "Produto criado com sucesso",
                "dados" : dados
            }), 201 
        return Controllers.Error(("Este produto ja esta criado!"), 400)
    
    
    def VerProdutos(page, limit):
        offset = (page - 1) * limit
        cursor.execute("SELECT COUNT (*) FROM produtos")
        quantidade_produto = cursor.fetchone()
        total_pages = quantidade_produto[0] / limit #0 = quantidade de produtos
        cursor.execute("SELECT produto, estoque, preco_venda, preco_compra FROM produtos LIMIT ? OFFSET ?", (limit, offset))
        dados_produtos = cursor.fetchall()
        lista_produtos = {}
        for produto in dados_produtos:
            nome, estoque, preco_venda, preco_compra = produto
            lista_produtos[nome] = {
                "estoque" : estoque,
                "preco_venda" : preco_venda,
                "preco_compra" : preco_compra
            }
        return jsonify({
            "status" : "sucesso",
            "page" : page,
            "limit" : limit,
            "total_page" : total_pages,
            "dados" : lista_produtos
        }), 200
        
    def EditarProduto(dados):
        if not dados:
            return Controllers.Error(("JSON nao enviado"),400)
        if "produto" not in dados:
            return Controllers.Error(("JSON nao enviado"),400)
        cursor.execute("SELECT id FROM produtos WHERE produto = ?", (dados['produto'],))
        checar_produto_existente = cursor.fetchone()
        if checar_produto_existente is None:
            return Controllers.Error(("Produto nao encontrado!"), 404)
        if "preco_venda" in dados:
            cursor.execute("UPDATE produtos SET preco_venda = ? WHERE produto = ?", (dados['preco_venda'], dados['produto']))
        if "preco_compra" in dados:
            cursor.execute("UPDATE produtos SET preco_compra = ? WHERE produto = ?", (dados['preco_compra'], dados['produto']))
        if "estoque" in dados:
            cursor.execute("UPDATE produtos SET estoque = ? WHERE produto = ?", (dados['estoque'], dados['produto']))
        conectar.commit()
        return jsonify({
            "status" : "sucesso",
            "mensagem" : "dados alterado com sucesso!"
        }), 200
        
        
    def DeletarProduto(dados):
        if not dados:
            return Controllers.Error(("JSON nao enviado"),400)
        if 'produto' not in dados:
            return Controllers.Error(("Produto nao enviado"),400)
        cursor.execute("SELECT id FROM produtos WHERE produto = ?", (dados['produto'],))
        checar_produto_existente = cursor.fetchone()
        if checar_produto_existente is None:
            return Controllers.Error(("Produto nao encontrado!"), 404)
        cursor.execute("DELETE FROM produtos WHERE produto = ?", (dados['produto'],))
        conectar.commit()
        return jsonify({
            "status" : "sucesso",
            "mensagem" : f"Produto: {dados['produto']} deletado com sucesso!"
        }), 200