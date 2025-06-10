from flask import Blueprint,request,jsonify

cuenta_bp= Blueprint('cuenta', __name__)

# simulación base de datos
datos_cuenta= {
    'nombre': '',
    'apellido': '',
    'email': '',
    'dni': '',
    'direccion': '',
    'timbre': '',
    'piso': ''
}

#2.1 Crear cuenta
@cuenta_bp.route('/api/cuenta', methods=['POST'])
def crear_cuenta():
    data=request.get_json()
    for campo in datos_cuenta:
        datos_cuenta[campo] = data.get(campo, '')
    return jsonify({"mensaje": "Cuenta creada.", "cuenta": datos_cuenta}), 200

#2.2 Mostrar datos
@cuenta_bp.route('/api/cuenta', methods=['GET'])
def mostrar_datos():
    return jsonify(datos_cuenta), 200

#2.3 Modificar campo en particular
@cuenta_bp.route('/api/cuenta/<campo>', methods=['PATCH'])
def modificar_cuenta(campo):
    data=request.get_json()
    if campo in datos_cuenta:
        datos_cuenta[campo] = data.get(campo, datos_cuenta[campo])
        return jsonify({"mensaje": f"{campo} modificado", "cuenta": datos_cuenta}), 200
    return jsonify({"error": "Campo no encontrado"}), 404

#2.4 Actualizar datos
@cuenta_bp.route('/api/cuenta/actualizar-datos', methods=['GET', 'POST'])
def actualizar_datos():
    if request.method == 'POST':
        data = request.get_json()
        for campo in datos_cuenta:
            if campo in datos_cuenta:
                datos_cuenta[campo]=data[campo]
    # Retornamos los datos actuales
    if request.method == 'GET':
       
        return jsonify({"mensaje":"Datos actualizados.", "cuenta": datos_cuenta}), 200
    return jsonify(datos_cuenta), 200

#2.5 Eliminar cuenta
@cuenta_bp.route('/api/cuenta', methods=['DELETE'])
def eliminar_cuenta():
    for campo in datos_cuenta:
        datos_cuenta[campo] = ''
    # Limpiamos los datos de la cuenta
    return jsonify({"mensaje": "Cuenta eliminada exitosamente."}), 200

def obtener_datos_cuenta():
    return datos_cuenta
