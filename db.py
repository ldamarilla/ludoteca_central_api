from flask import Flask, jsonify, request
from sqlalchemy import text, create_engine
from sqlalchemy.exc import SQLAlchemyError
from config import DATABASE_URI

engine = create_engine(DATABASE_URI)

def get_productos():
    if request.method == 'GET':
        query = """SELECT * FROM PRODUCTOS;"""

        products = list()

        with engine.connect() as conn:
            result = conn.execute(text(query))

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
    return None


def get_producto(id):
    query = f"""SELECT * FROM PRODUCTOS p WHERE p.id = '{id}';"""

    product = dict()

    with engine.connect() as conn:
        result = conn.execute(text(query))

        for row in result:
            product['id'] = row.ID
            product['nombre'] = row.NOMBRE
            product['precio'] = row.PRECIO
            product['stock'] = row.STOCK
            product['descripcion'] = row.DESCRIPCION
            product['categoria_id'] = row.CATEGORIA_ID

    return jsonify(product)

def add_producto():
    data = request.get_json()

    query = "INSERT INTO PRODUCTOS (NOMBRE, PRECIO, STOCK, DESCRIPCION, CATEGORIA_ID) VALUES (:nombre, :precio, :stock, :descripcion, :categoria_id);"

    product = dict()

    try:
        with (engine.connect() as conn):
            conn.execute(
                text(query),
                {
                    "nombre": data["nombre"],
                    "precio": data["precio"],
                    "stock": data["stock"],
                    "descripcion": data["descripcion"],
                    "categoria_id": data["categoria_id"]
                }
            )
            conn.commit()

        return jsonify({'message': 'Producto creado correctamente'}), 201

    except SQLAlchemyError as e:
        return jsonify({'error': 'Error en la base de datos', 'detalle': str(e)}), 500

    except Exception as e:
        return jsonify({'error': 'Error inesperado', 'detalle': str(e)}), 500
