from flask import Flask, jsonify, request, make_response
from sqlalchemy import text, create_engine
from sqlalchemy.exc import SQLAlchemyError
from config import DATABASE_URI
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import uuid
import usuario
from bcrypt import hashpw, checkpw, gensalt
from re import match
import re
import base64

engine = create_engine(DATABASE_URI)


def pull_data_db(query, params=None):
    with engine.connect() as conn:
        if params:
            return conn.execute(text(query), params)
        return conn.execute(text(query))

def push_data_db(query, data = None):
    with (engine.connect() as conn):
        conn.execute(
            text(query),
            data
        )
        conn.commit()

def modify_data_db(query, params=None):
    with engine.begin() as conn:  
        if params:
            return conn.execute(text(query), params)
        return conn.execute(text(query))

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

#PEDIDOS
def traer_pedidos():
    usuario_id = usuario.validar_token()
    if not usuario_id:
        return jsonify({'error': 'Token invalido o no proporcionado'}), 401
    try:
        query = """
                SELECT 
                    PEDIDOS.ID,
                    COMPRAS.ID,
                    COMPRAS.USUARIO_ID,
                    USUARIO.NOMBRE,
                    COMPRAS_PRODUCTOS.ID,
                    PRODUCTOS.NOMBRE,
                    COMPRAS_PRODUCTOS.CANTIDAD
                FROM PEDIDOS
                JOIN COMPRAS ON PEDIDOS.COMPRAS_ID = COMPRAS.ID
                JOIN USUARIO ON COMPRAS.USUARIO_ID = USUARIO.ID_USUARIO
                JOIN COMPRAS_PRODUCTOS ON COMPRAS_PRODUCTOS.COMPRA_ID = COMPRAS.ID
                                    AND COMPRAS_PRODUCTOS.PRODUCTO_ID = PEDIDOS.PRODUCTO_ID
                JOIN PRODUCTOS ON COMPRAS_PRODUCTOS.PRODUCTO_ID = PRODUCTOS.ID
            """
        filas = usuario.pull_data_db(query).fetchall()
        print(f"Filas obtenidas: {len(filas)}")

        if not filas:
            return jsonify({'error': 'No hay pedidos'}), 404

        pedidos = {}

        for row in filas:
            pedido_id = row[0]         
            compra_id = row[1]         
            usuario_id = row[2]        
            nombre_usuario = row[3]    
            producto_id = row[4]       
            producto_nombre = row[5]   
            cantidad = row[6]        

            if pedido_id not in pedidos:
                pedidos[pedido_id] = {
                    'pedido_id': pedido_id,
                    'compra_id': compra_id,
                    'usuario_id': usuario_id,
                    'nombre_usuario': nombre_usuario,
                    'productos': []
                }

            pedidos[pedido_id]['productos'].append({
                'producto_id': producto_id,
                'producto_nombre': producto_nombre,
                'cantidad': cantidad
            })


        return jsonify(pedidos), 200

    except Exception as e:
        print(f"[ERROR API /admin/mostrar-pedidos]: {e}")
        return jsonify({'error': 'Error inesperado'}), 500
    
def traer_productos():
    usuario_id = usuario.validar_token()
    if not usuario_id:
        return jsonify({'error': 'Token inválido o no proporcionado'}), 401

    try:
        query = """
            SELECT 
                PRODUCTOS.ID,
                PRODUCTOS.NOMBRE,
                PRODUCTOS.PRECIO,
                PRODUCTOS.STOCK,
                PRODUCTOS.DESCRIPCION,
                PRODUCTOS.IMAGEN,
                CATEGORIAS.ID AS CATEGORIA_ID,
                CATEGORIAS.NOMBRE AS CATEGORIA_NOMBRE
            FROM PRODUCTOS
            LEFT JOIN CATEGORIAS ON PRODUCTOS.CATEGORIA_ID = CATEGORIAS.ID
        """
        filas = usuario.pull_data_db(query).fetchall()

        if not filas:
            return jsonify({'error': 'No hay productos cargados'}), 404

        productos = []

        for row in filas:
            producto = {
                'id': row[0],
                'nombre': row[1],
                'precio': row[2] if row[3] is not None else 0,
                'stock': row[3] if row[3] is not None else 0,
                'descripcion': row[4],
                'imagen': row[5],  # base64 o ruta, según cómo lo guardes
                'categoria_id': row[6],
                'categoria_nombre': row[7]
            }
            productos.append(producto)

        return jsonify(productos), 200

    except Exception as e:
        print(f"[ERROR API /admin/productos]: {e}")
        return jsonify({'error': 'Error inesperado'}), 500

def eliminar_producto(producto_id):
    usuario_id = usuario.validar_token()
    if not usuario_id:
        return jsonify({'error': 'Token inválido'}), 401

    try:
        query = "DELETE FROM PRODUCTOS WHERE ID = :id;"
        params = {'id': producto_id}

        result = modify_data_db(query, params)  
        if result:
            return jsonify({'mensaje': 'Producto eliminado'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
def crear_producto():
    usuario_id = usuario.validar_token()

    if not usuario_id:
        return jsonify({'error': 'Token inválido'}), 401

    imagen = request.files.get('imagen')
    if not imagen or imagen.filename == '':
        return jsonify({'error': 'No se proporcionó imagen'}), 400

    filename = secure_filename(imagen.filename)
    ext = filename.rsplit('.', 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({'error': 'Tipo de archivo no permitido'}), 400

    image_b64 = base64.b64encode(imagen.read()).decode('utf-8')

    try:
        producto_data = {
            'nombre':        request.form.get('nombre'),
            'precio':        float(request.form.get('precio')),
            'stock':         int(request.form.get('stock')),
            'descripcion':   request.form.get('descripcion', ''),
            'categoria_id':  int(request.form.get('categoria_id')),
            'imagen':        image_b64
        }
    except (KeyError, ValueError) as e:
        return jsonify({'error': f'Datos inválidos: {e}'}), 400

    try:
        query = """
            INSERT INTO PRODUCTOS
                (NOMBRE, PRECIO, STOCK, DESCRIPCION, CATEGORIA_ID, IMAGEN)
            VALUES (:nombre, :precio, :stock, :descripcion, :categoria_id, :imagen)
        """
        result = modify_data_db(query, producto_data)
        producto_id = result.lastrowid
    except Exception as e:
        print(f"[ERROR API /admin/productos/agregar]: {e}")
        return jsonify({'error': 'Error inesperado'}), 500

    return jsonify({
        'producto_nuevo': producto_data,
        'imagen': {
            'nombre': filename,
            'base64': image_b64
        }
    }), 201

def actualizar_producto(producto_id):
    usuario_id = usuario.validar_token()
    if not usuario_id:
        return jsonify({'error': 'Token inválido'}), 401

    imagen = request.files.get('imagen')
    if not imagen or imagen.filename == '':
        return jsonify({'error': 'No se proporcionó imagen'}), 400

    filename = secure_filename(imagen.filename)
    ext = filename.rsplit('.', 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({'error': 'Tipo de archivo no permitido'}), 400

    image_b64 = base64.b64encode(imagen.read()).decode('utf-8')

    try:
        producto_data = {
            'id':            producto_id,
            'nombre':        request.form.get('nombre'),
            'precio':        float(request.form.get('precio')),
            'stock':         int(request.form.get('stock')),
            'descripcion':   request.form.get('descripcion', ''),
            'categoria_id':  int(request.form.get('categoria_id')),
            'imagen':        image_b64
        }
    except (KeyError, ValueError) as e:
        return jsonify({'error': f'Datos inválidos: {e}'}), 400

    try:
        query =""" 
                UPDATE PRODUCTOS
                SET NOMBRE = :nombre,
                    PRECIO = :precio,
                    STOCK = :stock,
                    DESCRIPCION = :descripcion,
                    CATEGORIA_ID = :categoria_id,
                    IMAGEN = :imagen
                WHERE ID = :id;
                """
        result = modify_data_db(query, producto_data)  
        if result:
            return jsonify({'mensaje': 'Producto actualizado'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400









    
