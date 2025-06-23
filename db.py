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
        product['imagen_url'] = row.IMAGEN
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
    product['imagen_url'] = result.IMAGEN

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
        product['imagen_url'] = row.IMAGEN
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

def update_stock_producto(id, cantidad):
    validation_producto_query = f"""SELECT ID FROM PRODUCTOS p WHERE ID ='{id}';"""
    validation_producto_result = pull_data_db(validation_producto_query).first()

    if not validation_producto_result:
        return jsonify({'error': 'Producto no hallado'}), 404

    query = f"""UPDATE PRODUCTOS SET stock='{cantidad}' WHERE ID ='{id}';"""

    try:
        push_data_db(query)
        return jsonify({'message': 'Actualización de stock ejecutada correctamente'}), 200

    except Exception as e:
        return jsonify({'error': 'Error inesperado', 'detalle': str(e)}), 500

def delete_producto(id):
    prod_query = f"""SELECT * FROM PRODUCTOS WHERE id='{id}';"""
    prod_result = pull_data_db(prod_query).first()

    if not prod_result:
        return jsonify({'error': 'No existe producto a eliminar'}), 404

    producto_a_eliminar_query = f"""DELETE FROM PRODUCTOS WHERE id='{id}';"""

    try:
        push_data_db(producto_a_eliminar_query)
        return jsonify({'message': 'Se eliminó el carrito y sus productos correctamente'}), 200

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
    validation_producto_result = (pull_data_db(f"""SELECT * FROM PRODUCTOS p WHERE ID ='{data['producto_id']}';""")
                                  .first())

    if not validation_producto_result: return jsonify({'error': 'Producto no hallado'}), 404

    compra_en_progreso_query = f"SELECT * FROM COMPRAS c WHERE FINALIZADA = false AND USUARIO_ID = '{data['usuario_id']}';"
    compra_en_progreso_result = pull_data_db(compra_en_progreso_query).first()

    if not compra_en_progreso_result:
       add_carrito_query = "INSERT INTO COMPRAS (FECHA, USUARIO_ID, FINALIZADA) VALUES (:fecha, :usuario_id, :finalizada);"
       compra_params = { "fecha": datetime.now(), "usuario_id": data['usuario_id'], "finalizada": False }
       push_data_db(add_carrito_query, compra_params)

    validation_producto_unique_result = (
        pull_data_db(f"""SELECT * FROM COMPRAS_PRODUCTOS cp WHERE PRODUCTO_ID ='{data['producto_id']}' AND COMPRA_ID ='{compra_en_progreso_result.ID}';""")
        .first())
    if validation_producto_unique_result: return jsonify({'error': 'Producto ya agregado al carrito'}), 422

    compra_en_progreso_result = pull_data_db(compra_en_progreso_query).first()
    add_producto_query = "INSERT INTO COMPRAS_PRODUCTOS (COMPRA_ID, PRODUCTO_ID, CANTIDAD) VALUES (:compra_id, :producto_id, :cantidad);"
    prod_params = {
        "compra_id": compra_en_progreso_result.ID,
        "producto_id": data["producto_id"],
        "cantidad": data["cantidad"]
    }

    try:
        push_data_db(add_producto_query, prod_params)
        return jsonify({'message': 'Se agrego el producto al carrito correctamente'}), 201

    except Exception as e:
        return jsonify({'error': 'Error inesperado', 'detalle': str(e)}), 500

def get_carrito():
    data = request.args.to_dict()
    carrito_producto_query = f"""SELECT * FROM COMPRAS c 
                                INNER JOIN COMPRAS_PRODUCTOS cp on cp.COMPRA_ID = c.ID
                                INNER JOIN PRODUCTOS p on p.ID = cp.PRODUCTO_ID
                                WHERE c.FINALIZADA = false AND USUARIO_ID = '{data['usuario_id']}';"""
    carrito_producto_results = pull_data_db(carrito_producto_query).fetchall()

    carrito_query = f"""SELECT * FROM COMPRAS WHERE FINALIZADA = false AND USUARIO_ID = '{data['usuario_id']}';"""
    carrito_result = pull_data_db(carrito_producto_query).first()

    if not carrito_result:
        add_carrito_query = "INSERT INTO COMPRAS (FECHA, USUARIO_ID, FINALIZADA) VALUES (:fecha, :usuario_id, :finalizada);"
        compra_params = {"fecha": datetime.now(), "usuario_id": data['usuario_id'], "finalizada": False}
        push_data_db(add_carrito_query, compra_params)
        carrito_result = pull_data_db(carrito_query).first()

    compra = dict()

    compra["id"] = carrito_result.ID
    compra["fecha"] = carrito_result.FECHA
    compra["usuario_id"] = carrito_result.USUARIO_ID

    compra["carrito_productos"] = list()

    for compra_prod in carrito_producto_results:
        compra_producto = dict()
        compra_producto["producto_id"] = compra_prod.PRODUCTO_ID
        compra_producto["producto_nombre"] = compra_prod.NOMBRE
        compra_producto["producto_precio"] = compra_prod.PRECIO
        compra_producto["producto_stock"] = compra_prod.STOCK
        compra_producto["producto_cantidad"] = compra_prod.CANTIDAD
        compra_producto["producto_descripcion"] = compra_prod.DESCRIPCION
        compra_producto["producto_imagen"] = compra_prod.IMAGEN
        compra["carrito_productos"].append(compra_producto)

    return jsonify(compra)

def delete_carrito_producto(producto_id):
    data = request.get_json()
    usuario_id = data['usuario_id']
    validation_producto_result = (pull_data_db(f"""SELECT * FROM PRODUCTOS p WHERE ID ='{producto_id}';""")
                                  .first())

    if not validation_producto_result:
        return jsonify({'error': 'Producto inexistente'}), 404

    validation_compra_producto_query = f"""SELECT cp.ID AS ID FROM COMPRAS_PRODUCTOS cp
                                    JOIN COMPRAS c ON c.ID=cp.COMPRA_ID
                                    WHERE c.FINALIZADA=false AND cp.PRODUCTO_ID='{producto_id}' AND c.USUARIO_ID='{usuario_id}';"""
    validation_compra_producto_result = pull_data_db(validation_compra_producto_query).first()

    if not validation_compra_producto_result:
        return jsonify({'error': 'Producto a eliminar no hallado en el carrito'}), 400

    query = f"""DELETE cp FROM COMPRAS_PRODUCTOS cp
            JOIN COMPRAS c ON c.ID=cp.COMPRA_ID
            WHERE c.FINALIZADA=false AND cp.PRODUCTO_ID='{producto_id}' AND c.USUARIO_ID='{usuario_id}';"""

    try:
        push_data_db(query)
        return jsonify({'message': 'Eliminación de producto en carrito ejecutada correctamente'}), 200

    except Exception as e:
        return jsonify({'error': 'Error inesperado', 'detalle': str(e)}), 500

def delete_carrito():
    data = request.get_json()
    print(data)
    query = f"""DELETE FROM COMPRAS WHERE USUARIO_ID='{data["usuario_id"]}' AND FINALIZADA=false;"""

    try:
        push_data_db(query)
        return jsonify({'message': 'Eliminación de carrito y todos sus productos ejecutada correctamente'}), 200

    except Exception as e:
        return jsonify({'error': 'Error inesperado', 'detalle': str(e)}), 500

