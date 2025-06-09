from flask import Flask
from flask_cors import CORS
from routes.alumnos import alumnos_bp
from routes.materias import materias_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(admin_bp, url_prefix="/vista-administrador-1")
app.register_blueprint(carrito_bp, url_prefix="/carrito")
app.register_blueprint(pedidos_bp, url_prefix="/pedidos")
app.register_blueprint(productos_bp, url_prefix="/categorias")
app.register_blueprint(usuario_bp, url_prefix="/crear-usuario")


if __name__ == "__main__":
    app.run(debug=True)