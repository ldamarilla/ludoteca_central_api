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
        query = """ SELECT ID, PRODUCTO_ID, COMPRAS_ID FROM PEDIDOS """
        pedidos = usuario.pull_data_db(query).fetchall()
        print(f"[DEBUG] Filas obtenidas: {len(pedidos)}")

        if not pedidos:
            return jsonify({'error': 'Aun no hay ningun pedido realizado'}), 404

        pedidos_dict = {
            row.ID: {
                'id' : row.ID,
                'producto' : row.PRODUCTO_ID,
                'compras' : row.COMPRAS_ID
                }
                for row in pedidos
            }
                
        return jsonify(pedidos_dict), 200
    
    except Exception as e:
        print(f"[ERROR API /admin/mostrar-pedidos]: {e}")
        return jsonify({'error': 'Error inesperado'}), 500