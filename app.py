from base64 import b64decode, b64encode
from flask import Flask, jsonify, request
import db, usuario, admin

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

@app.route('/api/carrito', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def carrito():
    if request.method == 'GET':
        return db.get_carrito()

    if request.method == 'POST':
        return db.add_producto_a_carrito()

    if request.method == 'PATCH':
        return db.update_cantidad_producto_carrito()

    if request.method == 'DELETE':
        return db.delete_carrito()

    return None

@app.route('/api/carrito/<producto_id>', methods=['DELETE'])
def carrito_producto(producto_id):
    if request.method == 'DELETE':
        return db.delete_carrito_producto(producto_id)
    return None


# PEDIDOS
@app.route('/api/pedidos', methods=['GET'])
def pedidos_usuario():
    return db.get_pedidos_por_usuario()

@app.route('/api/pedidos', methods=['GET'])
def pedidos():
    if request.method == 'GET':
        return db.get_all_pedidos()
    
@app.route('/api/compras/<compra_id>', methods=['GET'])
def get_compra(compra_id):
        return db.get_compra(compra_id)
    
@app.route('/api/compras/<compra_id>', methods=['PATCH'])
def fin_compra(compra_id):
    if request.method == 'PATCH':
        return db.finalizar_compra(compra_id)


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

@app.route('/api/mi-cuenta/cerrar-sesion', methods=['GET', 'POST'])
def cerrar_sesion():
    return usuario.cerrar_sesion()

@app.route('/api/mi-cuenta/eliminar', methods=['GET', 'DELETE', 'POST'])
def eliminar_micuenta():
    return usuario.eliminar_micuenta()

usuario.actualizar_contrasenias_no_hasheadas()

#ADMIN
@app.route('/api/admin/pedidos', methods=['GET', 'POST'])
def obtener_pedidos():
    return admin.traer_pedidos()



# SERVER
if __name__ == '__main__':
    print("Rutas activas:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint:25s} → {rule.rule}")

    app.run(port=5070, debug=True)
