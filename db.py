from flask import Flask, jsonify, request
from sqlalchemy import text, create_engine
from datetime import datetime
from config import DATABASE_URI
engine = create_engine(DATABASE_URI)

def pull_data_db(query):
    with engine.connect() as conn:
        return conn.execute(text(query))

def push_data_db(query, data = None):
    with (engine.connect() as conn):
        conn.execute(
            text(query),
            data
        )
        conn.commit()

# PRODUCTOS

def get_productos():
    query = "SELECT * FROM PRODUCTOS;"
    products = list()
    result = pull_data_db(query)

    for row in result:
        product = dict()
        product['id'] = row.ID
        product['nombre'] = row.NOMBRE
        product['precio'] = row.PRECIO
        product['stock'] = row.STOCK
        product['descripcion'] = row.DESCRIPCION
        product['categoria_id'] = row.CATEGORIA_ID
        products.append(product)

    return jsonify(products)

def get_producto(id):
    query = f"""SELECT * FROM PRODUCTOS p WHERE p.id = '{id}';"""
    product = dict()
    result = pull_data_db(query).first()

    if not result:
        return jsonify({'error': 'Item no hallado'}), 404

    product['id'] = result.ID
    product['nombre'] = result.NOMBRE
    product['precio'] = result.PRECIO
    product['stock'] = result.STOCK
    product['descripcion'] = result.DESCRIPCION
    product['categoria_id'] = result.CATEGORIA_ID

    return jsonify(product), 200

def get_productos_by_categoria(id):
    validation_categoria_query =  f"""SELECT ID FROM CATEGORIAS p WHERE ID ='{id}';"""
    validation_categoria_result = pull_data_db(validation_categoria_query).first()

    if not validation_categoria_result:
        return jsonify({'error': 'Categoría no hallada'}), 404

    query = f"""SELECT * FROM PRODUCTOS p WHERE categoria_id ='{id}';"""

    result = pull_data_db(query)

    products = list()
    for row in result:
        product = dict()
        product['id'] = row.ID
        product['nombre'] = row.NOMBRE
        product['precio'] = row.PRECIO
        product['stock'] = row.STOCK
        product['descripcion'] = row.DESCRIPCION
        product['categoria_id'] = row.CATEGORIA_ID
        products.append(product)
    return jsonify(products), 200

def add_producto():
    data = request.get_json()
    validation_categoria_query = f"""SELECT ID FROM CATEGORIAS p WHERE id ='{data['categoria_id']}';"""
    validation_categoria_result = pull_data_db(validation_categoria_query).first()

    if not validation_categoria_result:
        return jsonify({'error': 'Categoría no hallada'}), 404

    query = ("INSERT INTO PRODUCTOS (NOMBRE, PRECIO, STOCK, DESCRIPCION, CATEGORIA_ID) "
             "VALUES (:nombre, :precio, :stock, :descripcion, :categoria_id);")

    params = {
        "nombre": data["nombre"],
        "precio": data["precio"],
        "stock": data["stock"],
        "descripcion": data["descripcion"],
        "categoria_id": data["categoria_id"]
    }

    try:
        push_data_db(query, params)
        return jsonify({'message': 'Producto creado correctamente'}), 201

    except Exception as e:
        return jsonify({'error': 'Error inesperado', 'detalle': str(e)}), 500

def update_stock_producto(id):
    data = request.get_json()
    validation_producto_query = f"""SELECT ID FROM PRODUCTOS p WHERE ID ='{id}';"""
    validation_producto_result = pull_data_db(validation_producto_query).first()

    if not validation_producto_result:
        return jsonify({'error': 'Producto no hallado'}), 404

    query = f"""UPDATE PRODUCTOS SET stock='{data['stock']}' WHERE ID ='{id}';"""

    try:
        push_data_db(query)
        return jsonify({'message': 'Actualización de stock ejecutada correctamente'}), 200

    except Exception as e:
        return jsonify({'error': 'Error inesperado', 'detalle': str(e)}), 500


#CATEGORIAS

def get_categorias():
    query = "SELECT * FROM CATEGORIAS;"
    categorias = list()
    result = pull_data_db(query)

    for row in result:
        categoria = dict()
        categoria['id'] = row.ID
        categoria['nombre'] = row.NOMBRE
        categorias.append(categoria)

    return jsonify(categorias)

def get_categoria(id):
    query = f"""SELECT * FROM CATEGORIAS p WHERE p.id = '{id}';"""
    categoria = dict()

    result = pull_data_db(query).first()
    if not result:
        return jsonify({'error': 'Item no hallado'}), 404

    categoria['id'] = result.ID
    categoria['nombre'] = result.NOMBRE

    return jsonify(categoria)

def add_categoria():
    data = request.get_json()
    query = "INSERT INTO CATEGORIAS (NOMBRE) VALUES (:nombre);"
    params = { "nombre": data["nombre"] }

    try:
        push_data_db(query, params)
        return jsonify({'message': 'Categoria creada correctamente'}), 201

    except Exception as e:
        return jsonify({'error': 'Error inesperado', 'detalle': str(e)}), 500

#CARRITO

def add_producto_a_carrito():
    data = request.get_json()
    validation_producto_query = f"""SELECT ID FROM PRODUCTOS p WHERE id ='{data['producto_id']}';"""
    validation_producto_result = pull_data_db(validation_producto_query).first()

    if not validation_producto_result:
        return jsonify({'error': 'Producto no hallado'}), 404

    compra_en_progreso_query = "SELECT * FROM COMPRAS c WHERE FINALIZADA = false;"
    compra_en_progreso_result = pull_data_db(compra_en_progreso_query).first()

    if not compra_en_progreso_result:
       add_carrito_query = "INSERT INTO COMPRAS (FECHA, USUARIO_ID, FINALIZADA) VALUES (:fecha, :usuario_id, :finalizada);"
       compra_params = {
           "fecha": datetime.now(),
           "usuario_id": get_usuario_logueado()["ID"],
           "finalizada": False
       }
       push_data_db(add_carrito_query, compra_params)

    compra_en_progreso_result = pull_data_db(compra_en_progreso_query).first()
    add_producto_query = "INSERT INTO COMPRAS_PRODUCTOS (COMPRA_ID, PRODUCTO_ID, CANTIDAD) VALUES (:compra_id, :producto_id, :cantidad);"
    prod_params = {
        "compra_id": compra_en_progreso_result.ID,
        "producto_id": data["producto_id"],
        "cantidad": 1
    }

    try:
        push_data_db(add_producto_query, prod_params)
        return jsonify({'message': 'Se agrego el producto al carrito correctamente'}), 201

    except Exception as e:
        return jsonify({'error': 'Error inesperado', 'detalle': str(e)}), 500

def get_carrito():
    compra_en_progreso_query = f"""SELECT * FROM COMPRAS c 
                                LEFT JOIN COMPRAS_PRODUCTOS cp on cp.COMPRA_ID = c.ID
                                WHERE c.FINALIZADA = false;"""
    compra_en_progreso_results = pull_data_db(compra_en_progreso_query).fetchall()

    if not compra_en_progreso_results[0]:
        return jsonify({'error': 'Carrito no creado'}), 404

    compra = dict()

    compra["id"] = compra_en_progreso_results[0].ID
    compra["fecha"] = compra_en_progreso_results[0].FECHA
    compra["usuario_id"] = compra_en_progreso_results[0].USUARIO_ID

    compra["compra_productos"] = list()

    for compra_prod in compra_en_progreso_results:
        compra_producto = dict()
        compra_producto["producto_id"] = compra_prod.PRODUCTO_ID
        compra_producto["cantidad"] = compra_prod.CANTIDAD
        compra["compra_productos"].append(compra_producto)

    return jsonify(compra)

def get_usuario_logueado(): #mock, está harcodeado ahora
    usuario =  {
        "ID": 1
    }
    return jsonify(usuario)


