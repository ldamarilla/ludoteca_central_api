from flask import Blueprint, jsonify, request
from db import get_connection

usuario_bp = Blueprint("usuario", __name__)

@usuario_bp.route("/", methods=["POST"])
def agregar_datos_usuario():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    data = recuest.json