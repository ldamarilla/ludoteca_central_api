from flask import Flask, jsonify, request
from sqlalchemy import text, create_engine
from sqlalchemy.exc import SQLAlchemyError
from config import DATABASE_URI

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
        usuario['Email_usuario'] = row.EMAIL
        usuario['Contrasenia'] = row.CONTRASENIA

        
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
        'Email_usuario': result.EMAIL,
        'Contrasenia': result.CONTRASENIA
    }

    return jsonify(usuario), 200

def add_usuario():
    data = request.get_json()
    query = "INSERT INTO USUARIO (EMAIL,CONTRASENIA) VALUES (:Email_usuario, :Contrasenia);"
    params = { "Email_usuario": data["Email_usuario"],"Contrasenia": data["Contrasenia"] }

    try:
        push_data_db(query, params)
        return jsonify({'message': 'Usuario creado correctamente'}), 201

    except Exception as e:
        return jsonify({'error': 'Error inesperado', 'detalle': str(e)}), 500    