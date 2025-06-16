from base64 import b64decode, b64encode
from flask import Flask, jsonify, request, Blueprint, render_template, url_for
from sqlalchemy import create_engine, text
from config import DATABASE_URI
import re

loguear_cuenta_bp = Blueprint("loguear_cuenta", __name__)

engine = create_engine(DATABASE_URI)

@loguear_cuenta_bp.route("/", methods=["GET", "POST"])
def iniciarSesionAdmin():
    if request.method == "POST":
        try:
            email = request.form.get("email")
            contrasenia = request.form.get("contrasenia")

            if not email or not contrasenia:
                return render_template("error.html"), 400

            # Verificar si existe un usuario con ese email y contraseña
            query1 = text("""
                SELECT ID_ADMIN, NOMBRE_ADMIN FROM ADMIN
                WHERE EMAIL_ADMIN = :email AND CONTRASENIA = :contrasenia
            """)
            params = {"email": email, "contrasenia": contrasenia}

            with engine.connect() as conn:
                admin = conn.execute(query1, params).fetchone()

            if admin:
                # Login exitoso
                session["admin_id"] = admin["ID_ADMIN"]
                return render_template("vista-admin.html", nombre=admin["NOMBRE"]), 200
            else:
                # Email o contraseña incorrectos
                return render_template("error.html"), 401
            
        except Exception as e:
            print("Error durante el login:", e)
            return render_template("error.html"), 500

def iniciarSesionUsuario():
    if request.method == "POST":
        try:
            email = request.form.get("email")
            contrasenia = request.form.get("contrasenia")

            if not email or not contrasenia:
                return render_template("error.html"), 400

            # Verificar si existe un usuario con ese email y contraseña
            query1 = text("""
                SELECT ID_USUARIO FROM USUARIO
                WHERE EMAIL = :email AND CONTRASENIA = :contrasenia
            """)
            params = {"email": email, "contrasenia": contrasenia}

            with engine.connect() as conn:
                usuario = conn.execute(query1, params).fetchone()

            if usuario:
                # Login exitoso
                session["usuario_id"] = usuario["ID_USUARIO"]
                return redirect(url_for("sesion-iniciada"))
            else:
                # Email o contraseña incorrectos
                return render_template("error.html"), 401
            
        except Exception as e:
            print("Error durante el login:", e)
            return render_template("error.html"), 500
            