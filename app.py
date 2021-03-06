from flask import Flask, render_template, request, redirect, jsonify, send_file, session
from werkzeug.utils import redirect
import werkzeug.security as ws
import bd
from flask import make_response


app = Flask(__name__)
app.secret_key = 'mi_llave_secreta'

@app.before_request
def antes_peticion():
    if 'correo' not in session and request.endpoint in ['perfil']:
       return redirect('/')

    elif 'correo' in session and request.endpoint in ['login']:
        return redirect('/perfil/{}'.format(session['correo']))

@app.route('/')
def bienvenido():
    return render_template('welcome.html')
    

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')
    else: 
        #Validar los valores de los formularios de registro
        if request.form['boton-env'] == "anterior":
            nombre = request.form['nombre']
            apellido = request.form["apellido"]
            correo = request.form["correo"]
            contraseña = request.form["contraseña"]
            bd.insertar_usuario(nombre,apellido,correo,ws.generate_password_hash(contraseña))
            session['correo'] = correo
            return redirect('/perfil/{}'.format(correo))
        #Validar los valores de los formularios de inicio de sesión
        elif request.form['boton-env'] == "siguiente":
            correoIni = request.form['correo-ini']
            registro_usuario = bd.obtener_registro('Usuario', "correo='{}'".format(correoIni))
            contraseña_bd = registro_usuario[0][4]
            if registro_usuario is not None:
                contraIni = request.form["contra-ini"]
                contraseña_igual = ws.check_password_hash(contraseña_bd, contraIni)
                if contraseña_igual:
                    session['correo'] = correoIni
                    return redirect('/perfil/{}'.format(correoIni))
            return render_template('login.html')

#sesión de perfil de usuario       
@app.route('/perfil')
@app.route('/perfil/<correo>')
def perfil(correo=None):
    if correo:
        registro_usuario = bd.obtener_registro('Usuario', "correo='{}'".format(correo))
        if registro_usuario:
            
            id_usuario = registro_usuario[0][0]
            
            agregar = False
            if correo == session['correo']:
                agregar = True
            
            return render_template('perfil-usuario.html', correo = registro_usuario, agregar = agregar)     
    else:
        return render_template('perfil-usuario.html')        

@app.route('/perfil/dashboard')
def dashboard():
    return render_template('Dashboard.html')

@app.route('/perfil/bedrooms')
def bedrooms():
    return render_template('bedrooms.html')

@app.route('/perfil/bedrooms_actions', methods=['GET', 'POST'])
def bedroom_actions():

    if request.method == 'GET':

        habitaciones = bd.obtener_todos_registros('Habitacion')
        return render_template('bedroom-actions.html', habitaciones = habitaciones)

    else: 
        #Validar los valores de los formularios de registro
        if request.form['botonGuardarHabitacion'] == "guardarHabitacion":
            Nombre = request.form['Nombre']
            Baños = request.form["Baños"]
            Camas = request.form["Camas"]
            Huespedes = request.form["Huespedes"]
            Aire_Acondicionado = request.form["Aire_Acondicionado"]
            WiFi = request.form["WiFi"]
            Cocina= request.form["Cocina"]
            Precio_Noche = request.form["Precio_Noche"]
            bd.insertar_habitaciones(Nombre,Baños,Camas,Huespedes,Aire_Acondicionado,WiFi,Cocina,Precio_Noche)

            habitaciones = bd.obtener_todos_registros('Habitacion')

            return render_template('bedroom-actions.html', habitaciones = habitaciones)

@app.route('/bedrooms_actions_delete', methods=['GET', 'POST'])
def bedroom_actions_delete():
    
    if request.method == 'GET':
    
        habitaciones = bd.obtener_todos_registros('Habitacion')
        return render_template('bedroom-actions.html', habitaciones = habitaciones)

    else: 
        #Validar los valores de los formularios de registro
        if request.form['botonEliminarHabitacion'] == "eliminarHabitacion":
            bd.eliminar_habitaciones(request.form["idhabitacion"])

            habitaciones = bd.obtener_todos_registros('Habitacion')

            return render_template('bedroom-actions.html', habitaciones = habitaciones)

@app.route('/bedrooms_qualify', methods=['GET', 'POST'])
def bedroom_qualify():
    if request.method == 'GET':
        return render_template('bedroom-qualify.html')
    else: 
        #Validar los valores de los formularios de calificacion y comentarios
            estrella = request.form['estrellas']
            comentario = request.form['comentario']
            print(estrella)
            print(comentario)
            bd.insertar_reseña(estrella, comentario)
            #session['correo'] = correo
            return redirect('/bedrooms')
        #Validar los valores de los formularios de inicio de sesión
        

@app.route('/cerrar_sesion')
def cerrar_sesion():
    if 'correo' in session:
        session.pop('correo')
        return redirect('/')

@app.route('/bedrooms_actions_edit', methods=['GET', 'POST'])
def bedroom_actions_edit():

            idhabitacion = request.form["idhabitacionedit"]
            habitacionEdit = bd.obtener_habitacion_por_id(idhabitacion)
            return render_template('bedroom-actions-update.html', habitacionEdit = habitacionEdit)

@app.route("/bedrooms_actions_update", methods=["POST"])
def bedroom_actions_update():

    if request.form['botonActualizarHabitacion'] == "actualizarHabitacion":
        idhabitacion = request.form['idhabitacion']
        Nombre = request.form['Nombre']
        Baños = request.form["Baños"]
        Camas = request.form["Camas"]
        Huespedes = request.form["Huespedes"]
        Aire_Acondicionado = request.form["Aire_Acondicionado"]
        WiFi = request.form["WiFi"]
        Cocina= request.form["Cocina"]
        Precio_Noche = request.form["Precio_Noche"]
        bd.actualizar_habitaciones(Nombre,Baños,Camas,Huespedes,Aire_Acondicionado,WiFi,Cocina,Precio_Noche,idhabitacion)

        habitaciones = bd.obtener_todos_registros('Habitacion')

        return render_template('bedroom-actions.html', habitaciones = habitaciones)


@app.route('/perfil/welcome')
def bienvenido2():
    return render_template('welcome.html')