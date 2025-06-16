from flask import Flask, jsonify, request
from sqlalchemy import text, create_engine
from sqlalchemy.exc import SQLAlchemyError
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
    validation_categoria_query =  f"""SELECT ID FROM CATEGORIAS p WHERE id ='{id}';"""
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
