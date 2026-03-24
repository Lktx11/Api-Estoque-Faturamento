from flask import jsonify

class Controllers:

    def Error(mensagem, codigo):
        jsonify({
            "status" : "erro",
            "mensagem" : mensagem,
        }), codigo
        