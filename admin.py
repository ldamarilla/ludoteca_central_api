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