from base64 import b64decode, b64encode
from flask import Flask, jsonify, request
import usuario,db

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


# CARGAR USUARIO

@app.route('/api/usuario', methods=['GET', 'POST'])
def usuarios():
    if request.method == 'GET':
        return usuario.get_usuarios()

    if request.method == 'POST':
        return usuario.add_usuario()
    return None



#CARGAR DATOS EN MI CUENTA

@app.route('/api/usuario/<id>', methods=['GET','PUT','DELETE'])
def micuenta(id):

    if request.method == 'GET':
        return usuario.get_usuario(id)

    if request.method == 'PUT':
        return usuario.update_micuenta(id)
    
    if request.method == 'DELETE':
        return usuario.delete_micuenta(id)

    return None

#LOGIN

@app.route('/api/login', methods=['POST'])
def login ():

    if request.method == 'POST':
        return usuario.login_usuario()

    return None


@app.route('/api/protected', methods=['GET'])
def protected_route():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({'error': 'Token no proporcionado'}), 401

    try:
        token = auth_header.split(" ")[1]  # Asumiendo formato "Bearer <token>"
    except IndexError:
        return jsonify({'error': 'Formato de token inválido'}), 401

    user_data = validar_token(token)
    if not user_data:
        return jsonify({'error': 'Token inválido o expirado'}), 401

    return jsonify({'message': 'Acceso permitido', 'user': user_data}), 200


if __name__ == '__main__':
    app.run(port=5050, debug=True)