from base64 import b64decode, b64encode
from flask import Flask, jsonify, request
import usuario, uuid
from config import DATABASE_URI

app = Flask(__name__)


#USUARIO

@app.route('/api/usuario/crear', methods=['POST'])
def crear_cuenta():
        return usuario.crear_cuenta()

@app.route('/api/usuario/login', methods=['POST'])
def login_usuario():
    return usuario.login_usuario()

@app.route('/api/usuario/token', methods=['GET'])
def validar_token():
    return usuario.validar_token()



#MI CUENTA
@app.route('/api/mi-cuenta/traer-datos', methods=['GET', 'POST'])
def datos_micuenta():
    return usuario.datos_micuenta()

@app.route('/api/mi-cuenta/actualizar', methods=['GET','PATCH', 'POST'])
def actualizar_micuenta():
    return usuario.actualizar_micuenta()

@app.route('/api/mi-cuenta/eliminar', methods=['GET', 'DELETE', 'POST'])
def eliminar_micuenta():
    return usuario.eliminar_micuenta()


usuario.actualizar_contrasenias_no_hasheadas()

if __name__ == '__main__':
    app.run(port=5050, debug=True)