from flask import Flask
from flask_cors import CORS
from routes.crearUsuario import crearUsuario_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(crearUsuario_bp, url_prefix="/crear-usuario")

if __name__ == "__main__":
    app.run ("127.0.0.1", port = "5000", debug = True)