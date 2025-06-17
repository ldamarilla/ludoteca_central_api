from flask import Flask, jsonify, request
from sqlalchemy import text, create_engine
from sqlalchemy.exc import SQLAlchemyError
from config import DATABASE_URI

engine = create_engine(DATABASE_URI)

def pull_data_db(query, params=None):
    with engine.connect() as conn:
        return conn.execute(text(query), params)

def push_data_db(query, data = None):
    with (engine.connect() as conn):
        conn.execute(
            text(query),
            data
        )
        conn.commit()


def get_admins():
    query = "SELECT * FROM ADMIN;"
    admins = list()
    result = pull_data_db(query)

    for row in result:
        admin = dict()
        admin['id'] = row.ID_ADMIN
        admin['Nombre_admin'] = row.NOMBRE_ADMIN
        admins.append(admin)

    return jsonify(admins)



def get_admin(id):
    query = "SELECT * FROM ADMIN WHERE ID_ADMIN = :id;"
    result = pull_data_db(query, {'id': id}).first()

    if not result:
        return jsonify({'error': 'No existe Admin con ese ID'}), 404

    admin = {
        'id': result.ID_ADMIN,  
        'Nombre_admin': result.NOMBRE_ADMIN
    }

    return jsonify(admin), 200

