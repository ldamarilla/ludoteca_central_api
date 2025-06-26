from base64 import b64decode, b64encode
from flask import Flask, jsonify, request
import db, usuario, admin
from db import pull_data_db
import uuid
from config import DATABASE_URI
import os

app = Flask(__name__)

BASE_IMAGE_DIR = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

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
@app.route('/api/pedidos', methods=['GET', 'PATCH'])
def pedidos():
    if request.method == 'GET':
        return db.get_all_pedidos()
    if request.method == 'PATCH':
        return db.finalizar_compra()

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

@app.route('/api/admin/productos', methods=['GET', 'POST'])
def crear_producto():
    imagen_url = None
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        if imagen.filename != '':
            file_ext = imagen.filename.rsplit('.', 1)[-1].lower()
            if file_ext not in ALLOWED_EXTENSIONS:
                return jsonify({'error': 'Tipo de archivo no permitido'}), 400
            
            # Construir ruta CON verificación
            image_path = f"{BASE_IMAGE_DIR}/{file_ext}"
            
            # Prevenir directory traversal
            if not image_path.startswith(BASE_IMAGE_DIR):
                return jsonify({'error': 'Ruta de imagen inválida'}), 400
            
            try:
                with open(image_path, 'wb') as f:
                    f.write(imagen.read())
                imagen_url = f"/static/images/{file_ext}"
            except IOError as e:
                return jsonify({'error': f"Error al guardar imagen: {str(e)}"}), 500
            
    producto_data = {
        'nombre': request.form['nombre'],
        'precio': float(request.form['precio']),
        'stock': int(request.form['stock']),
        'descripcion': request.form.get('descripcion', ''),
        'categoria_id': int(request.form['categoria_id']),
        'imagen_url': imagen_url
            }
    try:
        query = """
        INSERT INTO PRODUCTOS (NOMBRE, PRECIO, STOCK, DESCRIPCION, CATEGORIA_ID, IMAGEN) VALUES
        (:nombre, :precio, :stock, :descipcion, :categoria_id,, :imagen_url)
        RETURNIG ID
        """
        result = pull_data_db(query, producto_data).first()
        return jsonify({
            'status': 'success',
            'producto_id': result[0],
            'imagen_url': imagen_url
        }), 201
    except Exception as e:
        # Limpieza en caso de error
        if imagen_url and os.path.exists(image_path):
            os.remove(image_path)
        return jsonify({'error': str(e)}), 500

# SERVER
if __name__ == '__main__':
    print("Rutas activas:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint:25s} → {rule.rule}")

    app.run(port=5070, debug=True)
