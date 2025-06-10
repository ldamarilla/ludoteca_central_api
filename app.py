from flask import Flask, render_template, request, redirect, url_for
from routes.cuenta import cuenta_bp, obtener_datos_cuenta

app= Flask(__name__)
app.register_blueprint(cuenta_bp)

@app.route('/mi-cuenta', methods=['GET', 'POST'])
def miCuenta():
    menuID = 'Mi cuenta'
    datos_cuenta=obtener_datos_cuenta()
    if request.method == 'POST':
        datos_cuenta['nombre'] = request.form.get('nombre', '')
        datos_cuenta['apellido'] = request.form.get('apellido', '')
        datos_cuenta['email'] = request.form.get('email', '')
        datos_cuenta['dni'] = request.form.get('dni', '')
        datos_cuenta['direccion'] = request.form.get('direccion', '')
        datos_cuenta['timbre'] = request.form.get('timbre', '')
        datos_cuenta['piso'] = request.form.get('piso', '')

        return redirect(url_for('micuenta'))
    return render_template('mi-cuenta.html', micuenta=datos_cuenta, menuID=menuID)