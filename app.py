from flask import Flask, render_template, url_for, redirect, request, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required, current_user
import requests

import os
from flask_mail import Mail
from flask_mail import Message

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='postgres://qkzigtnnwgatix:d42371c3df95181f15bef8e1e0f5ef2ec2f8076305db278dcfef720ede70c363@ec2-52-6-178-202.compute-1.amazonaws.com:5432/d4l74kfk7riufd'
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres:marcopolo123@localhost:5432/meteorologico'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
bcrypt = Bcrypt()
bcrypt.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.log_view='login'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'sender.adrian.141197@gmail.com'
app.config['MAIL_PASSWORD'] = 'maadem141197'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


#Index
@app.route('/',methods=['GET','POST'])
def index():
    busq=""
    params = {
            'access_key': 'e7cd1b2453a6b98d4aea423f1ea60b6a',
            'query': 'Colima'
        }
    api_result = requests.get('https://api.weatherstack.com/current', params)
    api_response = api_result.json()
    if request.method=='POST':
        busq = request.form['busqueda']
        print(busq)
        params = {
            'access_key': 'e7cd1b2453a6b98d4aea423f1ea60b6a',
            'query': busq
        }
        api_result = requests.get('https://api.weatherstack.com/current', params)
        api_response = api_result.json()
        #print(api_result)
        print(api_response)
        print(u'Current temperature in %s is %d℃' % (api_response['location']['name'], api_response['current']['temperature']))
        # Handle POST Request here
        if current_user.is_authenticated:
            ciudad = Ciudad.query.filter_by(nombre=busq).first()
            print(ciudad)
            if ciudad == None:
                city = Ciudad(nombre=busq)
                db.session.add(city)
                db.session.commit()
            ciudad = Ciudad.query.filter_by(nombre=busq).first()
            consulta = Consulta(
                id_usuario = current_user.id,
                id_ciudad = ciudad.id,
                fecha = datetime.now()
            )
            db.session.add(consulta)
            db.session.commit()
        return render_template('index.html',clima=api_response)
    return render_template('index.html',clima=api_response)

@app.route('/historial')
@login_required
def historial():
    registros = Consulta.query.filter_by(id_usuario=current_user.id)
    return render_template('historial.html',registros=registros)

@app.route('/acerca')
def acerca():
   return render_template('acerca.html')

@app.route('/perfil')
@login_required
def perfil():
   return render_template('perfil.html')

#login
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('login.html')
    return render_template('login.html')

@app.route('/loginin',methods=['GET','POST'])
def loginin():
    if request.method == 'POST':
        usuario = request.form['user']
        passw = request.form['pwd']
        usuario_existe = Usuario.query.filter_by(nusuario = usuario).first()
        print(usuario_existe)
        mensaje = usuario_existe.correo
        if usuario_existe != None:
            print("Existe")
            if bcrypt.check_password_hash(usuario_existe.passw,passw):
                print("Usuario Autenticado")
                login_user(usuario_existe)
                if current_user.is_authenticated:
                    flash("Inicio de Sesion Exitoso!")
                    return redirect("/")
        return render_template('login.html',mensaje=mensaje)
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Cierre de Sesion Exitoso")
    return redirect("/")
   

#register
@app.route('/register',methods=['GET','POST'])
def register():
    mensaje = ''
    if request.method=='POST':
        ncontra = request.form['ncontra']
        ncontrac = request.form['ncontrac']
        if ncontra != ncontrac:
            mensaje = "Contraseñas no coinciden!"
            return render_template('registro.html',mensaje=mensaje)
        else:
            user = request.form['nusuario']
            nnombre = request.form['nnombre']
            napellido = request.form['napellido']
            ncorreo = request.form['ncorreo']
            ncontras = request.form['ncontra']
            print(user,nnombre,napellido,ncorreo)
            usuario = Usuario(
                nusuario = user,
                nombre = nnombre,
                apellido = napellido,
                correo = ncorreo,
                passw = bcrypt.generate_password_hash(ncontras).decode('utf-8')
            )
            db.session.add(usuario)
            db.session.commit()
            #Enviar correo
            msg = Message("Gracias por registrarte en la nube!", sender="sender.adrian.141197@gmail.com", recipients=[ncorreo])
            msg.body = "Este es un email de prueba"
            msg.html = "<p>Gracias por registrarte en la pagina, este es un mensaje de verificacion</p>"
            mail.send(msg)
            flash("Usuario Registrado! Revise su correo")
            return redirect("/")
        # Handle POST Request here
        return render_template('registro.html')
    return render_template('registro.html')

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer,primary_key=True)
    nusuario = db.Column(db.String(20),nullable=False,unique=True,index=True)
    nombre  = db.Column(db.String(30),nullable=False)
    apellido = db.Column(db.String(30),nullable=False)
    correo = db.Column(db.String(100),nullable=False,unique=True,index=True)
    passw = db.Column(db.String(200),nullable=False)

    def __init__(self,nusuario,nombre,apellido,correo,passw):
        self.nusuario = nusuario
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.passw = passw
    
    def __repr__(self):
        return 'El usuario es {} con nombre {} {} y correo {}'.format(self.nusuario,self.nombre,self.apellido,self.correo)
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.filter_by(id=user_id).first()


class Ciudad(db.Model):
    __tablename__ = 'ciudad'
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(30),index=True)

    def __init__(self,nombre):
        self.nombre = nombre
    
    def __repr__(self):
        return 'La ciudad es: {}'.format(self.nombre)


class Consulta(db.Model):
    __tablename__ = 'consulta'
    id_usuario = db.Column(db.Integer,db.ForeignKey('usuario.id'),primary_key=True)
    id_ciudad = db.Column(db.Integer,db.ForeignKey('ciudad.id'),primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow,primary_key=True)

    def __init__(self,id_usuario,id_ciudad,fecha):
        self.id_usuario = id_usuario
        self.id_ciudad = id_ciudad
        self.fecha = fecha


if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    db.create_all()
    app.run(port=5000,debug=True)