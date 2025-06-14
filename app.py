from base64 import b64decode, b64encode
from flask import Flask, jsonify, request, Blueprint
from sqlalchemy import create_engine, text
from config import DATABASE_URI
from routes.crear_usuario import crear_usuario_bp
from routes.vista_admin_1 import vista_admin_1_bp
from routes.logear_cuenta import loguear_cuenta_bp

app = Flask(__name__)

app.register_blueprint(crear_usuario_bp, url_prefix="/crear_usuario")
app.register_blueprint(admin_bp, url_prefix="/vista_administrador_1")
app.register_blueprint(loguear_cuenta_bp, url_prefix="/inicio-sesion")

if __name__ == '__main__':
    app.run(port=8081, debug=True)