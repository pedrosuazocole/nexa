from flask import Flask, render_template, request, redirect, url_for, session, abort
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'cambia-esta-clave-por-una-muy-larga-y-secreta'


USUARIO = 'admin'
PASSWORD = '1234'


IPS_PERMITIDAS = ['127.0.0.1', '192.168.1.100','10.1.1.133','10.1.1.7']  

notificacionescaja = []
notificacionespir = []

def validar_mensaje(mensaje):
    return True if mensaje else False

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')
        if usuario == USUARIO and password == PASSWORD:
            session['usuario'] = usuario
            return redirect(url_for('panel'))
        else:
            return render_template('login.html', error='Credenciales incorrectas')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inicio'))

@app.route('/panel')
def panel():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('panel.html', notificacionescaja=notificacionescaja, notificacionespir=notificacionespir)

@app.route('/notificacioncaja', methods=['POST'])
def recibir_notificacion_caja():
    ip_remota = request.remote_addr
    if ip_remota not in IPS_PERMITIDAS:
        abort(403)  
    mensaje = request.form.get('mensaje', 'Sin mensaje')
    if not validar_mensaje(mensaje):
        abort(400)  
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    notificacionescaja.append(f"[{timestamp}] {mensaje}")
    print(f"Notificación recibida: {mensaje} desde {ip_remota}")
    return 'OK'

@app.route('/notificacionpir', methods=['POST'])
def recibir_notificacion_pir():
    ip_remota = request.remote_addr
    if ip_remota not in IPS_PERMITIDAS:
        abort(403)  
    mensaje = request.form.get('mensaje', 'Sin mensaje')
    if not validar_mensaje(mensaje):
        abort(400) 
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    notificacionespir.append(f"[{timestamp}] {mensaje}")
    print(f"Notificación recibida: {mensaje} desde {ip_remota}")
    return 'OK'

if __name__ == "__main__":

    app.run(debug=True, host='0.0.0.0', port=5001)
