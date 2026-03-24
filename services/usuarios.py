from services.controllers import Controllers


class Usuarios:

    def Registrar(dados):
        if not dados:
            return Controllers.Error(("JSON nao enviado"), 404)
        return f"funfou"