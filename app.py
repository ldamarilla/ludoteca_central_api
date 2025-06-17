from base64 import b64decode, b64encode
from flask import Flask, jsonify, request
import admin,db

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


# VER ADMIN

@app.route('/api/ver-admin', methods=['GET'])
def get_admins():
    return admin.get_admins()


@app.route('/api/ver-admin/<id>', methods=['GET'])
def get_admin(id):
    return admin.get_admin(id)



if __name__ == '__main__':
    app.run(port=5050, debug=True)