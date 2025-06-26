from flask import Flask, jsonify, request, make_response
from sqlalchemy import text, create_engine
from sqlalchemy.exc import SQLAlchemyError
from config import DATABASE_URI
from datetime import datetime, timedelta
import uuid
import usuario
from bcrypt import hashpw, checkpw, gensalt
from re import match
import re

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
        JOIN PRODUCTOS ON COMPRAS_PRODUCTOS.PRODUCTO_ID = PRODUCTOS.ID

        """
        filas = usuario.pull_data_db(query).fetchall()

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
    

#CARGAR

def cargar_productos():
    try:
        # Obtener datos del request
        data = request.get_json()
        nombre_producto = data.get("nombre_producto")
        precio = data.get("precio")
        stock = data.get("stock")
        descripcion = data.get("descripcion")
        categoria_id = data.get("categoria_id")

        # Validar datos obligatorios
        if not all([nombre_producto, precio, stock, descripcion, categoria_id]):
            return jsonify({'error': 'Faltan datos obligatorios'}), 400

        # Verificar que la categoría exista
        categoria_query = "SELECT COUNT(*) FROM CATEGORIAS WHERE ID = :categoria_id;"
        categoria_result = pull_data_db(categoria_query, {"categoria_id": categoria_id}).scalar()

        if categoria_result == 0:
            return jsonify({'error': f'La categoría con ID {categoria_id} no existe'}), 400

        # Insertar el producto en la base de datos
        insert_query = """
        INSERT INTO PRODUCTOS (NOMBRE, PRECIO, STOCK, DESCRIPCION, CATEGORIA_ID)
        VALUES (:nombre_producto, :precio, :stock, :descripcion, :categoria_id);
        """
        insert_params = {
            "nombre_producto": nombre_producto,
            "precio": precio,
            "stock": stock,
            "descripcion": descripcion,
            "categoria_id": categoria_id
        }
        push_data_db(insert_query, insert_params)

        return jsonify({'mensaje': 'Producto agregado con éxito'}), 201

    except Exception as e:
        # Manejo de errores generales
        print(f"[ERROR]: {e}")
        return jsonify({'error': str(e)}), 500

    

#EDITAR
def actualizar_producto():
    try:
        data = request.get_json()
        producto_id = data.get("producto_id")
        if not producto_id:
            return jsonify({'error': 'El ID del producto es obligatorio'}), 400

        columnas_map = {
            "nombre_producto": "NOMBRE",
            "precio": "PRECIO",
            "stock": "STOCK",
            "descripcion": "DESCRIPCION",
            "categoria_id": "CATEGORIA_ID"
        }


        params = {k: v for k, v in data.items() if k in columnas_map and v is not None}
        params["producto_id"] = producto_id

        if len(params) <= 1:  
            return jsonify({'error': 'No se proporcionaron datos para actualizar'}), 400

        set_clause = ", ".join([f"{columnas_map[key]} = :{key}" for key in params if key != "producto_id"])

        query = f"""
        UPDATE PRODUCTOS
        SET {set_clause}
        WHERE ID = :producto_id;
        """

        result = modify_data_db(query, params)
        if result.rowcount == 0:
            return jsonify({'error': 'El producto no existe o no se pudo actualizar'}), 404

        return jsonify({'mensaje': 'Producto actualizado correctamente'}), 200

    except Exception as e:
        print(f"[ERROR API /admin/productos/actualizar_producto]: {e}")
        return jsonify({'error': 'Error inesperado', 'detalle': str(e)}), 500
    



#ELIMINAR

def eliminar_producto():
    try:
        data = request.get_json()
        producto_id = data.get('producto_id')  # O cambia según cómo recibas el id

        if not producto_id:
            return jsonify({'error': 'El ID del producto es obligatorio'}), 400

        query = "DELETE FROM PRODUCTOS WHERE ID = :producto_id;"
        params = {'producto_id': producto_id}

        result = modify_data_db(query, params)
        if result.rowcount == 0:
            return jsonify({'error': 'No fue posible eliminar el producto correctamente'}), 400

        return jsonify({'mensaje': 'Producto eliminado correctamente'}), 200

    except Exception as e:
        print(f"[ERROR API /admin/productos/eliminar_producto]: {e}")
        return jsonify({'error': 'Ha sucedido un error inesperado', 'detalle': str(e)}), 500

    
