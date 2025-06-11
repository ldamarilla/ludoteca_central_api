from base64 import b64decode, b64encode
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
from config import DATABASE_URI

app = Flask(__name__)

engine = create_engine(DATABASE_URI)

@app.route('/api/productos', methods=['GET', 'POST'])
def productos():
    if request.method == 'GET':
        return get_productos()

    if request.method == 'POST':
        return "add_producto"
    return None


@app.route('/api/productos/<id>', methods=['GET'])
def get_product(id):
    return get_producto(id)

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
                product['id_categoria'] = row.CATEGORIA_ID

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
            product['id_categoria'] = row.CATEGORIA_ID

    return jsonify(product)

if __name__ == '__main__':
    app.run(port=5050, debug=True)