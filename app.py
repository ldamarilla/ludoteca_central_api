from base64 import b64decode, b64encode
from flask import Flask, jsonify, request, Blueprint
from sqlalchemy import create_engine, text
from config import DATABASE_URI
from routes.crearUsuario import crearUsuario_bp
from routes.admin import admin_bp

app = Flask(__name__)

app.register_blueprint(crearUsuario_bp, url_prefix="/crear-usuario")
app.register_blueprint(admin_bp, url_prefix="/vista-administrador-1")

if __name__ == '__main__':
    app.run(port=8081, debug=True)