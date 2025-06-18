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
def login():
    return usuario.login_usuario()


#URL DE PRUEBA PARA VER SI EL TOKEN FUNCIONA PARA OBTENER LOS DATOS DEL USUARIO LOGUEADO
@app.route("/api/pruebaLogueado", methods=["GET"])
def token():
    return usuario.traer_token()


if __name__ == '__main__':
    app.run(port=5050, debug=True)