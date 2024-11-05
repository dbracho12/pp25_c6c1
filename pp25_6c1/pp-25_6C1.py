# Alumno:
# El objetivo es realizar un ejercicio muy similar al
# realizado en el pasado con la API de jsonplaceholder.
# Deberan consumir toda la información que retorna
# el request de la API y almacenarla en una db.
# url = https://jsonplaceholder.typicode.com/todos
# Luego deberá crear una serie de endpoints
# para consultar la información almacenada
# en la base de datos
# En este desafio solo se utilizarán endpoints
# con HTTP GET (no se utilizará POST)
import traceback
import requests
from flask import Flask, request, jsonify, render_template, Response

#Base de dato
from flask_sqlalchemy import SQLAlchemy


#Crear el server Flask
app = Flask(__name__)

## Indicamos al sistema (app) de donde leer la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///libros.db"
db = SQLAlchemy()
db.init_app(app)
url = "https://jsonplaceholder.typicode.com/todos"
# ------------ Base de datos ----------------- #

# Deberá generar una base de datos SQL
# que posea los siguientes campos:
# - id --> [número] id de la consulta
# - userId --> [número] id del usuario
# - titulo --> [texto] nombre del título
# - completado --> [bool] completado o no el título
class Libro(db.Model):
    __tablename__ = "libros"
    id = db.Column(db.Integer, primary_key = True)
    userId= db.Column(db.Integer)
    titulo = db.Column(db.String)
    completado = db.Column(db.Boolean)

    def __repr__(self):
        return f"Usuario {self.userId} Titulo {self.titulo} Completado {self.completado}"


# ------------ Rutas o endpoints ----------------- #
@app.route("/")
def endpoints():
    try:
        result = "<h1>Bienvenido!!</h1>"
        result += "<h2> Se general los siguientes endpoints disponibles:</h2>"
        result += "<h3>[GET] /iniciar --> mostrar todo los datos  en formato JSON"
        result += "<h3>[GET] /usuarios --> mostrar todo los datos  en formato JSON"
        result += "<h3>[GET] /usuarios/[userId] --> mostrar todo los datos  en formato JSON"
        return result
    except:
        # En caso de falla, retornar el mensaje de error
        return jsonify({'trace': traceback.format_exc()})
# A)
# Ruta que se ingresa por la ULR 127.0.0.1:5000/iniciar
# Crear un endpoint para "iniciar" en el cual
# 1) Deberá vaciar la base de datos y volverla a crear
# 2) Utilizar requests para consumir toda la información
# de jsonplaceholder utilizando la URL indicanda al comienzo
# del enunciado
# 3) Utilizar un bucle para guardar esa información recolectada
# (una por una) en la base de datos
# 4) Retornar al frontend un texto que lo ayude a usted a
# comprender que la ruta se completó con éxito
# IMPORTANTE: Esta no es una buena forma de insertar datos,
# debe utilizarse un endpoint de POST para estas prácticas
# como se vio en clase. Pero ahora, para facilitar la práctica
# utilizaremos este recurso
    
@app.route("/iniciar")
def iniciar():
     try:
        # 1) Deberá vaciar la base de datos y volverla a crear 
        db.drop_all()
        db.create_all()
        # 2) Utilizar requests para consumir toda la información de jsonplaceholder utilizando la URL indicanda al comienzo del enunciado
        response = requests.get(url)
        # 3) Utilizar un bucle para guardar esa información recolectada (una por una) en la base de datos
        
        resul_datos = []
        for dato in response:
            carga_dato = {}
            carga_dato['userId']=dato.userId
            carga_dato['titulo']=dato.titulo
            carga_dato['completado']=dato.completado
            resul_datos.append(carga_dato)
        
            return jsonify(resul_datos)

        # 4) Retornar al frontend un texto que lo ayude a usted a comprender que la ruta se completó con éxito
        if response.status_code == 200:
            return ("Datos recibido corectamente")
        else:
            return f"Error en la solicitud. Código de estado: {response.status_code}"

     except:
      #En caso de falla, retornar el mensaje de error
        return jsonify({'trace': traceback.format_exc()})

# B)
# Ruta que se ingresa por la ULR 127.0.0.1:5000/usuarios
# Crear un endpoint usuarios en el cual: recibe el userId
# 1) Deberá buscar en la base de datos todos los usuarios
# 2) Deberá armar una lista de todos los usuarios según
# el userId (sin duplicar)
# 3) Deberá retornar al frontend un JSON que tenga la lista
# de usuarios respetando esta estructura:
# [
#    {"userId": ...},
#    {"userId": ...},
# ]
# Cada elemento de esa lista (cada diccionario dentro de la lista)
# representa cada usuario en la base de datos.
# Esta lista debería retornar 10 elementos, porque
# en los datos de jsonplaceholder hay 10 usuarios (10 userId distintos)
@app.route("/usuario")
def usuarios():
    try:
        usuarios_url = requests.get(url)
        userId_result = []

        for dato_userId in usuarios_url:
            carga_userId = {}
            carga_userId['userId'] = dato_userId.userId
            userId_result.append(carga_userId)
        return jsonify(userId_result)
    except:
        return jsonify({'trace': traceback.format_exc()})
  


# C)
# Ruta que se ingresa por la ULR 127.0.0.1:5000/usuarios/<userId>
# Crear un endpoint usuarios/<userId> el cual recibe el userId
# del usuario que se desea consultar.
# 1) Deberá buscar en la base de datos todos los títulos
# completados por ese usuario según el userId
# Para realizar esta operación utilice filter de ORM
# 2) Deberá contar cuantos títulos completó ese usuario
# y almacenar ese valor en una variable llamda "titulos_completados"
# 3) Deberá retornar al frontend un JSON que tenga la siguiente
# estructura:
# {"userId": userId, "titulos_completados": titulos_completados}
@app.route("/usuarios/<userId>")
def usuarios(userId):
    try:
       query = db.session.query(Libro).filter(Libro.userId==userId).first()
       if query:
           titulos_completados= query.completado 

           return jsonify({"userId": userId, "titulos_completados": titulos_completados})
       else:
           return jsonify({"error": "Usuario no encontrado"})
    except:
        return jsonify({'trace': traceback.format_exc()})


#Programa principal
if __name__ == '__main__':
    print('¡Inove@Server start!')

        # Lanzar server
    app.run(host="127.0.0.1", port=5000)