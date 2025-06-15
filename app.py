from base64 import b64decode, b64encode
from flask import Flask, jsonify, request
import db

from config import DATABASE_URI

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(port=5050, debug=True)