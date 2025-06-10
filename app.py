from flask import Flask
from flask_cors import CORS
from routes.crearUsuario import crearUsuario_bp
from routes.admin import admin_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(crearUsuario_bp, url_prefix="/crear-usuario")
app.register_blueprint(crearUsuario_bp, url_prefix="/vista-administrador-1")


if __name__ == "__main__":
    app.run ("127.0.0.1", port = "5000", debug = True)