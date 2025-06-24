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
            COMPRAS_PRODUCTOS.NOMBRE,
            COMPRAS_PRODUCTOS.CANTIDAD

        FROM PEDIDOS

        JOIN COMPRAS ON PEDIDOS.COMPRAS_ID = COMPRAS.ID
        JOIN USUARIO ON COMPRAS.USUARIO_ID = USUARIO.ID_USUARIO
        JOIN COMPRAS_PRODUCTOS ON COMPRAS_PRODUCTOS.COMPRA_ID = COMPRAS.ID
        JOIN PRODUCTOS ON COMPRAS_PRODUCTOS.PRODUCTO_ID = COMPRAS_PRODUCTOS.ID
        """
        filas = usuario.pull_data_db(query).fetchall()

        if not filas:
            return jsonify({'error': 'No hay pedidos'}), 404

        pedidos = {}

        for row in filas:
            pid = row.pedido_id
            if pid not in pedidos:
                pedidos[pid] = {
                    'pedido_id': pid,
                    'compra_id': row.compra_id,
                    'usuario_id': row.USUARIO_ID,
                    'nombre_usuario': row.nombre_usuario,
                    'productos': []
                }
            pedidos[pid]['productos'].append({
                'producto_id': row.producto_id,
                'producto_nombre': row.producto_nombre,
                'cantidad': row.CANTIDAD
            })

        return jsonify(pedidos_dict), 200

    except Exception as e:
        print(f"[ERROR API /admin/mostrar-pedidos]: {e}")
        return jsonify({'error': 'Error inesperado'}), 500