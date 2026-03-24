
class Controllers:

    def Error(mensagem, codigo):
        return{
            "status" : "erro",
            "mensagem" : mensagem,
        }, codigo
        