from base64 import b64decode, b64encode
from flask import Flask, jsonify, request, Blueprint, render_template
from sqlalchemy import create_engine, text
import re

loguear_cuenta_bp = Blueprint("loguear_cuenta", __name__)

engine = create_engine(DATABASE_URI)

@loguear_cuenta_bp.route("/", methods=["GET", "POST"])
def iniciarSesion():
    if request.method == "POST":
        try:
            email = request.form.get("email")
            contrasenia = request.form.get("contrasenia")

            # Verificar si existe un usuario con ese email y contraseña
            query1 = text("""
                SELECT ID_USUARIO, NOMBRE FROM USUARIO 
                WHERE EMAIL = :email AND CONTRASENIA = :contrasenia
            """)
            params = {"email": email, "contrasenia": contrasenia}

            with engine.connect() as conn:
                result = conn.execute(query1, params).fetchone()

            if result:

                # Login exitoso
                return redirect("vista-admin.html", nombre=result["NOMBRE"]), 200
            else:
                # Email o contraseña incorrectos
                return render_template("error.html"), 401
            
        except Exception as e:
            print("Error durante el login:", e)
            return render_template("error.html"), 500
            