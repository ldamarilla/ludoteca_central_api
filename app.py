from base64 import b64decode, b64encode
from flask import Flask, jsonify, request
import usuario,db, uuid
from config import DATABASE_URI

app = Flask(__name__)

# PRODUCTOS
@app.route('/api/productos', methods=['GET', 'POST'])
def productos():
    if request.method == 'GET':
        return db.get_productos()

    if request.method == 'POST':
        return db.add_producto()
    return None

@app.route('/api/productos/<id>', methods=['GET'])
def get_product(id):
    return db.get_producto(id)

# CATEGORIAS
@app.route('/api/categorias', methods=['GET', 'POST'])
def categorias():
    if request.method == 'GET':
        return db.get_categorias()

    if request.method == 'POST':
        return db.add_categoria()
    return None

@app.route('/api/categorias/<id>', methods=['GET'])
def get_categoria(id):
    return db.get_categoria(id)


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

@app.route('/api/mi-cuenta/modificar', methods=['GET','PUT','DELETE', 'POST'])
def micuenta(id):
    accion = request.form.get('accion')
    if accion == 'PATCH':
        return usuario.actualizar_micuenta()
    elif accion == 'DELETE':
        return usuario.eliminar_micuenta()





if __name__ == '__main__':
    app.run(port=5050, debug=True)