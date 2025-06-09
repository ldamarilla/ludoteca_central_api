from flask import Flask
from flask_cors import CORS
from routes.admin import admin_bp
from routes.carrito import carrito_bp
from routes.pedidos import pedidos_bp
from routes.productos import productos_bp
from routes.usuario import usuario_bp


app = Flask(__name__)
CORS(app)

app.register_blueprint(admin_bp, url_prefix="/vista-administrador-1")
app.register_blueprint(carrito_bp, url_prefix="/carrito")
app.register_blueprint(pedidos_bp, url_prefix="/pedidos")
app.register_blueprint(productos_bp, url_prefix="/categorias")
app.register_blueprint(usuario_bp, url_prefix="/crear-usuario")


if __name__ == "__main__":
    app.run(debug=True)