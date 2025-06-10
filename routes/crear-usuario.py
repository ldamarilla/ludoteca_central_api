from flask import Blueprint, jsonify, request
from db import get_connection

crearUsuario_bp = Blueprint("crearUsuario", __name__)

@crearUsuario_bp.route("/", methods=["POST"])
def agregar_datos_usuario():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
    data = request.json
    if not data:
        return jsonify({"error": "Se esperaba un JSON con email y contrasenia."}), 400

    email = data.get("email")
    contrasenia = data.get("contrasenia")
    #Verificar que ambos campos tengas valores ingresados
    if not email or not contrasenia:
        return jsonify({"error": "Email y contrasenia son campos obligatorios."}), 400


    #Verificar si el email ya existe
    cursor.execute("SELECT ID_USUARIO FROM USUARIO WHERE EMAIL = %s", (email,))
    if cursor.fetchone():
        return jsonify({"error": "Este email ya está registrado."}), 409 # Conflicto

    cursor.execute("""
                INSERT INTO USUARIO (EMAIL, CONTRASENIA)
                VALUES (%s, %s)
                """, (email, contrasenia)) # Usar hashed_contrasenia aquí

    conn.commit()
    return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201

    except mysql.connector.Error as err:
        # Captura errores específicos de MySQL
        print(f"Error de base de datos: {err}")
        return jsonify({"error": "Error al registrar el usuario en la base de datos."}), 500
    except Exception as e:
        # Captura cualquier otro error inesperado
        print(f"Error inesperado: {e}")
        return jsonify({"error": "Ocurrió un error inesperado."}), 500
    finally:
        cursor.close()
        conn.close()


