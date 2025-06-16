from base64 import b64decode, b64encode
from flask import Flask, jsonify, request, Blueprint, render_template
from sqlalchemy import create_engine, text
from config import DATABASE_URI
import re

crear_usuario_bp = Blueprint("crear_usuario", __name__)

engine = create_engine(DATABASE_URI)

@crear_usuario_bp.route("/", methods=["GET", "POST"])
def agregar_datos_usuario():
    if request.method == "POST":
        try:
            email = request.form.get("email")
            contrasenia = request.form.get("contrasenia")


            #Verificar si el email ya existe
            query = text("SELECT ID_USUARIO FROM USUARIO WHERE EMAIL = :email")
            params = {"email": email}

            with engine.connect() as conn:
                result = conn.execute(query, params)

            if result.fetchone():
                return render_template("error.html"), 409 # Conflicto

            # Validar formato de email simple
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return render_template("error.html"), 400

            #Crear usuario
            query = text("INSERT INTO USUARIO (EMAIL, CONTRASENIA) VALUES (:email, :contrasenia)")
            params = {"email": email, "contrasenia": contrasenia}

            with engine.begin() as conn:
                conn.execute(query, params)

            return render_template('Usuario_creado.html'), 201

        except Exception as e:
                # Captura cualquier error inesperado
                print(f"Error inesperado: {e}")
                return render_template('Error_500.html'), 500

