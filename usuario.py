from flask import Flask, jsonify, request
from sqlalchemy import text, create_engine
from sqlalchemy.exc import SQLAlchemyError
from config import DATABASE_URI
from datetime import datetime, timedelta
import uuid

engine = create_engine(DATABASE_URI)

tokens_activos = {}

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
    # Verifica si la solicitud es JSON y si completan 'Email' y 'Contrasenia' 
    if not data:
        return jsonify({'error': 'No se proporcionó cuerpo JSON en la solicitud'}), 400

    email = data.get("Email")
    contrasenia_ingresada = data.get("Contrasenia")

    # Verifica que las credenciales no estén vacías
    if not email or not contrasenia_ingresada:
        return jsonify({'error': 'Faltan credenciales (email o contraseña)'}), 400

    # SQL para obtener email y contrasenia; pasamos parametros
    query = "SELECT ID_USUARIO, EMAIL, CONTRASENIA FROM USUARIO WHERE EMAIL = :email;"
    params = {'email': email}
    result = pull_data_db(query, params).first()

    # Verifica si se encontró un usuario y si la contraseña coincide
    # Se accede a la contraseña por su índice (2)
    if not result or result[2] != contrasenia_ingresada:
        return jsonify({'error': 'Email o contraseña incorrectos'}), 401

    #Crea el token y asigna el id del usuario logueado a ese token
    token = str(uuid.uuid4())
    id_usuario = result[0]
    query2 = """ INSERT INTO TOKEN_USUARIO (TOKEN, ID_USUARIO)
                VALUES (:token, :id_usuario); """
    params2 = {"token": token, "id_usuario": id_usuario}
    result2 = pull_data_db(query2, params2)

    if not result2:
        return jsonify({'error': 'Error al subir el token a la base de datos'}), 401

    return jsonify({'message': 'Login exitoso', 'id_usuario': result[0], 'Token': token}), 200

#FUNCION DE PRUEBA PARA EL TOKEN AL LOGUEAR 
def perfil():
    #----------INICIO BLOQUE TOKEN----------
    tokenn = request.headers.get("Authorization") #Obtiene el token del encabezado 'Authorization'
    if not tokenn:  #Verifica Authorization
        return jsonify({"error": "Token no proporcionado. Se requiere encabezado Authorization."}), 401
    if not tokenn.startswith('Bearer '): #Verifica y extrae el token del formato "Bearer <token>"
        return jsonify({"error": "Formato de token inválido. Use 'Bearer <token>'."}), 401
    token = tokenn.split(' ')[1] #Extrae solo la parte del token (UUID)
    #Selecciona el usuario con el token y verifica que exista
    query = """SELECT TOKEN, ID_USUARIO FROM TOKEN_USUARIO WHERE TOKEN = :token_param"""
    params = {"token_param": token} 

    try:
        result = pull_data_db(query, params).first()
    except Exception as e:
        return jsonify({"error": "eRROR AL VALIDAR"}), 500

    if not result:
        return jsonify({"error": "Usuario con token no encontrado"}), 401
    #----------FIN BLOQUE TOKEN----------

    #Obtene el ID del usuario asociado al token
    usuario_id = result[0]

    #SQL para buscar los datos del usuario orrespondiente al id guardado
    query2 = """SELECT ID_USUARIO, EMAIL, CONTRASENIA, NOMBRE, DIRECCION, PISO,
                TIMBRE, APELLIDO, DNI, ADMIN
                FROM USUARIO
                WHERE ID_USUARIO = :usuario_id;"""
    params2 = {"usuario_id": usuario_id}
    result2 = pull_data_db(query2, params2).first()

    #Verificar si se encontró el usuario en la base de datos
    if not result:
        return jsonify({"error": "Usuario asociado al token no encontrado en la base de datos."}), 404

    #Datos del usuario correspondiente al id guardado
    usuario_data = {
        "ID_USUARIO": result[0],
        "EMAIL": result[1],
        "CONTRASENIA": result[2],
        "NOMBRE": result[3],
        "DIRECCION": result[4],
        "PISO": result[5],
        "TIMBRE": result[6],
        "APELLIDO": result[7],
        "DNI": result[8],
        "ADMIN": result[9]
    }

    return jsonify(usuario_data), 200

