from base64 import b64decode, b64encode
from flask import Flask, jsonify, request
import db

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

@app.route('/api/productos/<id>', methods=['GET', 'PATCH', 'DELETE'])
def product(id):
    if request.method == 'GET':
        return db.get_producto(id)

    if request.method == 'PATCH':
        data = request.get_json()
        return db.update_stock_producto(id, data['stock'])

    if request.method == 'DELETE':
        return db.delete_producto(id)
    return None

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

@app.route('/api/categorias/<id>/productos', methods=['GET'])
def get_productos_by_categoria(id):
    return db.get_productos_by_categoria(id)

@app.route('/api/carrito', methods=['GET', 'POST', 'DELETE'])
def carrito():
    if request.method == 'GET':
        return db.get_carrito()

    if request.method == 'POST':
        return db.add_producto_a_carrito()

    if request.method == 'DELETE':
        return db.delete_carrito()

    return None

@app.route('/api/carrito/<producto_id>', methods=['DELETE'])
def carrito_producto(producto_id):
    if request.method == 'DELETE':
        return db.delete_carrito_producto(producto_id)
    return None


# PEDIDOS
@app.route('/api/pedidos/usuario/<usuario_id>', methods=['GET'])
def pedidos_usuario(usuario_id):
    return db.get_pedidos_por_usuario(usuario_id)

@app.route('/api/pedidos', methods=['GET', 'PATCH'])
def pedidos():
    if request.method == 'GET':
        return db.get_all_pedidos()
    if request.method == 'PATCH':
        return db.finalizar_compra()

# SERVER
if __name__ == '__main__':
    app.run(port=5070, debug=True)