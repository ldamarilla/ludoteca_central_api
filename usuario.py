from flask import Flask, jsonify, request, make_response
from sqlalchemy import text, create_engine
from sqlalchemy.exc import SQLAlchemyError
from config import DATABASE_URI
from datetime import datetime, timedelta
import uuid
from bcrypt import hashpw, checkpw, gensalt

engine = create_engine(DATABASE_URI)


def pull_data_db(query, params=None):
    with engine.connect() as conn:
        if params:
            return conn.execute(text(query), params)
        return conn.execute(text(query))

def push_data_db(query, data = None):
    with (engine.connect() as conn):
        conn.execute(
            text(query),
            data
        )
        conn.commit()

def modify_data_db(query, params=None):
    with engine.begin() as conn:  
        if params:
            return conn.execute(text(query), params)
        return conn.execute(text(query))

#------------------------------Funciones de usuario-------------------------------------
def crear_cuenta():
    data = request.get_json()

    email = data.get("Email")
    contrasenia = data.get("Contrasenia")
    
    try:
        if not email or not contrasenia:
            return jsonify({'error': 'Faltan datos obligatorios (Email y/o Contrasenia)'}), 400

        check_query = "SELECT COUNT(*) AS count FROM USUARIO WHERE EMAIL = :Email;"
        check_params = {"Email": email}
        result = pull_data_db(check_query, check_params).first()

        if result and len(result) > 0 and result[0] > 0:
            return jsonify({'error': 'Email en uso'}), 409
            
        hashed_password = hashpw(contrasenia.encode(), gensalt()).decode()

        insert_query = "INSERT INTO USUARIO (EMAIL, CONTRASENIA, ADMIN) VALUES (:Email, :Contrasenia, :ADMIN);"
        insert_params = {
            "Email": email,
            "Contrasenia": hashed_password,
            "ADMIN": data.get("ADMIN", 0)
        }
        
        result2 = push_data_db(insert_query, insert_params)
        return jsonify({'mensaje': 'Usuario creado correctamente'}), 201
    
    except SQLAlchemyError as e:
        print(f"[ERROR API /usuario/crear]: {e}")
        return jsonify({'error': 'Error en la base de datos', 'detalle': str(e)}), 500
    except Exception as e:
        print(f"[ERROR API /usuario/crear]: {e}")
        return jsonify({'error': 'Error en la base de datos', 'detalle': str(e)}), 500

def login_usuario():
    data = request.get_json()

    email = data.get("Email")
    contrasenia = data.get("Contrasenia")

    try:
        if not email or not contrasenia:
            return jsonify({'error': 'Faltan credenciales (email o contraseña)'}), 400

        query = "SELECT ID_USUARIO, EMAIL, CONTRASENIA, ADMIN FROM USUARIO WHERE EMAIL = :email;"
        params = {'email': email}
        result = pull_data_db(query, params).first()

        if not result or not checkpw(contrasenia.encode(), result[2].encode()):
            return jsonify({'error': 'Email o contraseña incorrectos'}), 409

        token = str(uuid.uuid4())
        id_usuario = result[0]
        admin_usuario = result[3]

        query2 = """ INSERT INTO TOKEN_USUARIO (TOKEN, ID_USUARIO)
                    VALUES (:token, :id_usuario); """
        params2 = {"token": token, "id_usuario": id_usuario}
        result2 = modify_data_db(query2, params2)
        
        if not result2:
            return jsonify({'error': 'Error al subir el token a la base de datos'}), 401

        return jsonify({
            'mensaje': 'Login exitoso',
            'token': token,
            'rol': 'admin' if admin_usuario else 'usuario'
        }), 200

    except SQLAlchemyError as e:
        print(f"[ERROR API /usuario/crear]: {e}")
        return jsonify({'error': 'Error en la base de datos', 'detalle': str(e)}), 500
    except Exception as e:
        print(f"[ERROR API /usuario/crear]: {e}")
        return jsonify({'error': 'Error en la base de datos', 'detalle': str(e)}), 500
    
def validar_token():
    token = request.cookies.get("token") or request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:  
        return None 

    query = """SELECT ID_USUARIO FROM TOKEN_USUARIO WHERE TOKEN = :token_param"""
    params = {"token_param": token}

    try:
        result = pull_data_db(query, params).first()
    except Exception:
        return None

    if not result:
        return None

    usuario_id = result[0]
    return usuario_id

#------------------------------Funciones de mi cuenta-------------------------------------
def datos_micuenta():
    usuario_id = validar_token()
    if not usuario_id:
        return jsonify({'error': 'Token invalido o no proporcionado'}), 401

    try:
        query = """ SELECT NOMBRE, APELLIDO, EMAIL, DNI, DIRECCION, PISO, TIMBRE 
                    FROM USUARIO WHERE ID_USUARIO = :id """
        params = {"id": usuario_id}
        usuario = pull_data_db(query, params).first()

        if not usuario:
            return jsonify({'error': 'Error al traer los datos'}), 401

        data_usuario = {
            'nombre': usuario[0],
            'apellido': usuario[1],
            'email': usuario[2],
            'dni': usuario[3],
            'direccion': usuario[4],
            'piso': usuario[5],
            'timbre': usuario[6]
        }
        return jsonify(data_usuario), 200
    
    except Exception as e:
        print(f"[ERROR API /mi-cuenta/traer-datos]: {e}")
        return jsonify({'error': 'Error inesperado'}), 500

def actualizar_micuenta():
    usuario_id = validar_token()
    if not usuario_id:  
        return jsonify({"error": "Error al traer los datos"}), 401

    try: 
        data = request.form
        if not data.get("Email"):
            return jsonify({'error': 'El campo Email es obligatorio'}), 400

        query = """ 
                    UPDATE USUARIO
                    SET 
                        EMAIL = :Email,
                        NOMBRE = :Nombre,
                        APELLIDO = :Apellido,
                        DIRECCION = :Direccion,
                        PISO = :Piso,
                        DNI = :DNI,
                        TIMBRE = :Timbre
                    WHERE ID_USUARIO = :ID_usuario;
                """
        params = {
            "ID_usuario": usuario_id,
            "Email": data.get("Email") or None,
            "Nombre": data.get("Nombre") or None,
            "Apellido": data.get("Apellido") or None,
            "Direccion": data.get("Direccion") or None,
            "Piso": data.get("Piso") or None,
            "DNI": data.get("Dni") or None,
            "Timbre": data.get("Timbre") or None
        }

        result = modify_data_db(query, params)
        if result.rowcount == 0:
            return jsonify({'error': 'Un error ha sucesido. Intente de nuevo.'}), 400
        return jsonify({'mensaje': 'Datos del usuario actualizados correctamente.'}), 200

    except Exception as e:
        print(f"[ERROR API /mi-cuenta/actualizar]: {e}")
        return jsonify({'error': 'Error inesperado', 'detalle': str(e)}), 500

def eliminar_micuenta():
    usuario_id = validar_token()
    if not usuario_id:  
        return jsonify({"error": "Error al traer los datos"}), 401

    try:
        query = "DELETE FROM TOKEN_USUARIO WHERE ID_USUARIO = :id;"
        params = {'id': usuario_id}
        query2 = "DELETE FROM USUARIO WHERE ID_USUARIO = :id;"

        result = modify_data_db(query, params)
        result2 = modify_data_db(query2, params)
        if not result or not result2:
            return jsonify({'error': 'No fue posible eliminar el usuario correctamente'}), 400
        return jsonify({'mensaje': 'Usuario eliminado correctamente'}), 200

    except Exception as e:
        print(f"[ERROR API /mi-cuenta/eliminar]: {e}")
        return jsonify({'error': 'Ha sucedido un error inesperado', 'detalle': str(e)}), 500

    return jsonify({'error': 'Error inesperado'}), 500
    



