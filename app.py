from flask import Flask, render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from flask_bcrypt import Bcrypt

app = Flask(__name__)
Bootstrap(app)
#app.config['SQLALCHEMY_DATABASE_URI']='postgres://qkzigtnnwgatix:d42371c3df95181f15bef8e1e0f5ef2ec2f8076305db278dcfef720ede70c363@ec2-52-6-178-202.compute-1.amazonaws.com:5432/d4l74kfk7riufd'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres:marcopolo123@localhost:5432/meteorologico'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
bcrypt = Bcrypt()
bcrypt.init_app(app)

#Index
@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('index.html')
    return render_template('index.html')

@app.route('/historial')
def historial():
   return 'Historial'

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
        print("Login in")

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
                passw = bcrypt.generate_password_hash(ncontras)
            )
            db.session.add(usuario)
            db.session.commit()
            mensaje = "Usuario registrado!"
            return render_template('index.html',mensaje=mensaje)
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


class Ciudad(db.Model):
    __tablename__ = 'ciudad'
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(30))
    codigoPostal = db.Column(db.Integer)

    def __init__(self,nombre,codigoPostal):
        self.nombre = nombre
        self.codigoPostal = codigoPostal
    
    def __repr__(self):
        return 'La ciudad es: {} con código postal: {}'.format(self.nombre,self.codigoPostal)


class Consulta(db.Model):
    __tablename__ = 'consulta'
    id_usuario = db.Column(db.Integer,db.ForeignKey('usuario.id'),primary_key=True)
    id_ciudad = db.Column(db.Integer,db.ForeignKey('ciudad.id'),primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow,primary_key=True)


if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    db.create_all()
    app.run(port=5000,debug=True)