from flask import Flask, jsonify, request
from werkzeug.security import check_password_hash
from sqlalchemy import text, create_engine
from sqlalchemy.exc import SQLAlchemyError
from config import DATABASE_URI
import jwt
from datetime import datetime, timedelta

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


def get_usuarios():
    query = "SELECT * FROM USUARIO;"
    usuarios = list()
    result = pull_data_db(query)

    for row in result:
        usuario = dict()
        usuario['id'] = row.ID_USUARIO
        usuario['Email'] = row.EMAIL
        usuario['Contrasenia'] = row.CONTRASENIA
        usuario['ADMIN']=row.ADMIN

        
        usuarios.append(usuario)

    return jsonify(usuarios)

def get_usuario(id):
    query = "SELECT * FROM USUARIO WHERE ID_USUARIO = :id;"
    params = {'id': id}
    result = pull_data_db(query, params).first()
    
    if not result:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    usuario = {
        'id': result.ID_USUARIO,
        'Email': result.EMAIL,
        'Contrasenia': result.CONTRASENIA
    }

    return jsonify(usuario), 200

def add_usuario():
    data = request.get_json()
    query = "INSERT INTO USUARIO (EMAIL,CONTRASENIA,ADMIN) VALUES (:Email, :Contrasenia, :ADMIN);"
    params = { "Email": data["Email"],"Contrasenia": data["Contrasenia"],"ADMIN": data.get("ADMIN", 0)  }

    try:
        push_data_db(query, params)
        return jsonify({'message': 'Usuario creado correctamente'}), 201

    except Exception as e:
        return jsonify({'error': 'Error inesperado', 'detalle': str(e)}), 500    
    



def update_micuenta(id):
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
        "ID_usuario": id,
        "Email": data["Email"],
        "Nombre": data["Nombre"],
        "Apellido": data["Apellido"],
        "Direccion": data["Direccion"],
        "Piso": data["Piso"],
        "DNI": data["DNI"],
        "Timbre": data["Timbre"]
    }

    try:
        push_data_db(query, params)
        return jsonify({'message': 'Datos del usuario actualizados correctamente'}), 200

    except Exception as e:
        return jsonify({'error': 'Error inesperado', 'detalle': str(e)}), 500



def delete_micuenta(id):
    query = "DELETE FROM USUARIO WHERE ID_USUARIO = :id;"
    params = {'id': id}

    try:
        push_data_db(query, params)
        return jsonify({'message': f'Usuario con ID {id} eliminado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': 'Error al eliminar usuario', 'detalle': str(e)}), 500
    

def login_usuario():
    data = request.get_json()
    email = data.get("Email")
    contrasenia_ingresada = data.get("Contrasenia")

    if not email or not contrasenia_ingresada:
        return jsonify({'error': 'Faltan credenciales (email o contraseña)'}), 400

    query = "SELECT ID_USUARIO, EMAIL, CONTRASENIA FROM USUARIO WHERE EMAIL = :email;"
    params = {'email': email}
    result = pull_data_db(query, params).first()

    if not result or result.CONTRASENIA != contrasenia_ingresada:
        return jsonify({'error': 'Email o contraseña incorrectos'}), 401

    # Generar token JWT sin expiración
    token = jwt.encode(
        {"id": result.ID_USUARIO, "email": result.EMAIL},
        "clave_secreta",  # Cambia esto por una clave segura
        algorithm="HS256"
    )
    return jsonify({'message': 'Inicio de sesión exitoso', 'token': token}), 200


def validar_token(token):
    try:
        decoded = jwt.decode(token, "clave_secreta", algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
