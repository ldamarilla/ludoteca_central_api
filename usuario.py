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
        return jsonify({'message': 'Usuario creado correctamente'}), 201
    
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
    token = request.cookies.get("token") 
    if not token:  
        return jsonify({"error": "Token no proporcionado."}), 401
    
    query = """SELECT ID_USUARIO FROM TOKEN_USUARIO WHERE TOKEN = :token_param"""
    params = {"token_param": token}

    try:
        result = pull_data_db(query, params).first()
    except Exception as e:
        return jsonify({"error": "Error al validar"}), 500

    if not result:
        return jsonify({"error": "Usuario con token no encontrado"}), 401

    usuario_id = result[0]

    return usuario_id, 200

#------------------------------Funciones de mi cuenta-------------------------------------
def update_micuenta():
    usuario_id = validar_token()
    if not usuario_id:  
        return jsonify({"error": "Error al traer los datos"}), 401

    try: 
        data = request.get_json()
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
            "Email": data["Email"] or None,
            "Nombre": data["Nombre"] or None,
            "Apellido": data["Apellido"] or None,
            "Direccion": data["Direccion"] or None,
            "Piso": data["Piso"] or None,
            "DNI": data["DNI"] or None,
            "Timbre": data["Timbre"] or None
        }

        result = push_data_db(query, params)
        if not result:
            return jsonify({'message': 'Un error ha sucesido. Intente de nuevo.'}), 400
        return jsonify({'message': 'Datos del usuario actualizados correctamente.'}), 200

    except Exception as e:
        return jsonify({'error': 'Error inesperado', 'detalle': str(e)}), 500

def delete_micuenta():
    usuario_id = validar_token()
    if not usuario_id:  
        return jsonify({"error": "Error al traer los datos"}), 401

    try:
        query = "DELETE FROM USUARIO WHERE ID_USUARIO = :id;"
        params = {'id': usuario_id}

        result = push_data_db(query, params)
        if not result:
            return jsonify({'message': 'No fue posible eliminar el usuario correctamente'}), 400
        return jsonify({'message': 'Usuario eliminado correctamente'}), 200

    except Exception as e:
        return jsonify({'error': 'Ha sucesido un error inesperado', 'detalle': str(e)}), 500
    



