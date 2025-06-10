from flask import Blueprint, jsonify, request
from db import get_connection


admin_bp = Blueprint("admin", __name__)

datos_cuenta= {
    'nombre_admin': '',
}


@admin_bp.route('/api/cuenta_admin', methods=['GET'])
def mostrar_nombre():
    return jsonify(datos_cuenta), 200