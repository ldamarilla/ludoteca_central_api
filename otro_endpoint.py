@app.route("/perfil", methods=["GET"])
def perfil():
    # Guarda el token del usuario logueado
    token = request.headers.get("Authorization")

    #verifica que la variable token tenga algun valor o que el mismo exista en tokens_activos
    if not token or token not in tokens_activos:
        return jsonify({"error": "Token inválido o ausente"}), 401

    #guarda el id del usuario al que le pertenece el token
    user_id = tokens_activos[token]

    # Buscar usuario por por el id previamente almacenado
    usuario = next((u for u in usuarios.values() if u["id"] == user_id), None)

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({ "id": usuario["ID_USUARIO"] })
