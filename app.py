from flask import Flask, render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres:marcopolo123@localhost:5432/meteorologico'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

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
        return render_template('index.html')
    return render_template('index.html')

#register
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('index.html')
    return render_template('index.html')

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer,primary_key=True)
    nusuario = db.Column(db.String(20),nullable=False,Index=True)
    nombre  = db.Column(db.String(30),nullable=False)
    apellido = db.Column(db.String(30),nullable=False)
    correo = db.Column(db.String(100),nullable=False,unique=True)

    def __init__(self,nusuario,nombre,apellido,correo):
        self.nusuario = nusuario
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
    
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
    id_usuario = db.Column(db.Integer,primary_key=True,db.ForeignKey('usuario.id'))
    id_ciudad = db.Column(db.Integer,primary_key=True,db.ForeignKey('ciudad.id'))
    fecha = db.Column(db.DateTime, default=datetime.now(tz='UTC'),primary_key=True)


if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    db.create_all()
    app.run(port=5000,debug=True)