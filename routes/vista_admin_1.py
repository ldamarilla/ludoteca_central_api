from base64 import b64decode, b64encode
from flask import Flask, jsonify, request, Blueprint, render_template
from sqlalchemy import create_engine, text
from config import DATABASE_URI
import re

vista_admin_1_bp = Blueprint("vista_admin_1", __name__)

engine = create_engine(DATABASE_URI)

@vista_admin_1_bp.route("/", methods=["GET"])
def mostrar_nombreadmin():
    if request.method == "GET":
        try:
            # Consulta a la base de datos
            query = text("SELECT ID_ADMIN FROM ADMIN WHERE EMAIL_ADMIN = ':email_admin'")
            with engine.connect() as connection:
                result = connection.execute(query).fetchone()
                
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            


        