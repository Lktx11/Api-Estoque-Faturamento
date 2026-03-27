from flask import Flask
from database.models.produtos.produtos import CriarProdutosDB
from database.models.vendas.vendas import CriarVendasDB
from database.models.usuarios.usuarios import CriarUsuariosDB
from database.models.idempontecy.idempotency_key import CriarIdempotencyDB
from database.models.token.token import CriarTokenDB
CriarTokenDB()
CriarIdempotencyDB()
CriarProdutosDB()
CriarVendasDB()
CriarUsuariosDB()
app = Flask(__name__)
import routes.routes



app.run()