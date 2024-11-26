from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models.platillo import db, Platillo
import os

app = Flask(__name__)

UPLOAD_FOLDER="./static/images"
app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/recetario'
app.config['SQLALCHEMY_TRACK_MODFICATIONS']=False

# Inicializar la extensión de SQLAlchemy
db.init_app(app)

# Crear la base de datos y sus tablas
with app.app_context():
    db.create_all()

# Base de datos temporal
usuarios = []
recetas = [
    {
        'titulo': 'Ensalada César',
        'ingredientes': 'Lechuga romana, crutones, queso parmesano, aderezo César',
        'instrucciones': 'Mezcla todos los ingredientes en un tazón y sirve fresco.',
        'imagen': 'ensalada_cesar.jpg'
    },
    {
        'titulo': 'Pizza Margherita',
        'ingredientes': 'Masa de pizza, salsa de tomate, mozzarella, albahaca',
        'instrucciones': 'Extiende la masa, añade los ingredientes y hornea a 220°C por 15 minutos.',
        'imagen': 'pizza_margherita.jpg'
    },
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/listado")
def name():
    platillos= Platillo.query.all()
    return render_template('listado.html', platillos=platillos)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/add_platillo', methods=['GET', 'POST'])
def add_platillo():
    titulo = request.form["titulo"]
    ingrediente = request.form["ingrediente"]
    instruccion = request.form["instruccion"]
    image = request.files["image"]
    url_image= image.filename
    if image:
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], image.filename))

    new_platillo= Platillo(titulo=titulo, ingrediente=ingrediente, instruccion=instruccion, image=url_image)
    db.session.add(new_platillo)
    db.session.commit()

    return redirect(url_for("register"))

if __name__ == '__main__':
    app.run(debug=True)
