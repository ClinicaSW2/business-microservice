from flask import Flask,jsonify,request
from sqlalchemy.orm import Session
from db import get_db
from controllerReservation import fetch_all_users,fetch_all_reservacion,promedio_atencion,suma_ingreso_mes_anio,suma_ingreso_mes_anioByEspecialidad
from flask_cors import CORS
from controllerReservation import  get_especialidades,promedio_atencion,suma_cantidad_mes_anioByEspecialidad,promedio_atencionF,promedio_atencionM



app = Flask(__name__)
CORS(app)  # Esto permitirá todas las solicitudes CORS desde cualquier origen


@app.route("/users", methods=["GET"])
def read_users():
    users_response = fetch_all_users()
    return jsonify(users_response)

@app.route("/powerBI", methods=["GET"])
def read_reservacion():
    reservacion_response = fetch_all_reservacion()
    return jsonify(reservacion_response)


@app.get("/promedioatencion")
def get_promedio_atencion():
    data = request.get_json()
    
    respuesta = promedio_atencion(data)
    return jsonify(respuesta),200



@app.get("/")
def hello_world():
    return jsonify({"res":"true","message":"todo ok!"})



@app.get("/user")
def getUsers():
    return jsonify({"Users":"Todos los usuarios estan aqui"})

@app.get("/sumaingresobymesbyanio")
def get_suma_ingreso_mes_anio():
    respuesta = suma_ingreso_mes_anio()
    return respuesta,200


#Envia los tados con la suma de los incresos por mes y por anio filtro por especialidad
@app.get("/sumaingresobymesbyanioByEspecialidad")
def get_suma_ingreso_mes_anioFilEspecilidad():
    especialidad = request.args.get('especialidad') 
    respuesta = suma_ingreso_mes_anioByEspecialidad(especialidad)
    return respuesta,200


#Sacar todo los especialidades que existen
@app.get("/getespecialidad")
def get_especialidad():
    respuesta = get_especialidades()
    return respuesta,200




#Sacar promedio de atencion
@app.get("/promedioAtencion")
def promedioAtencion():
    respuesta = promedio_atencion()
    return respuesta,200

#Sacar promedio de atencion
@app.get("/promedioAtencionM")
def promedioAtencionM():
    respuesta = promedio_atencionM()
    return respuesta,200

@app.get("/promedioAtencionF")
def promedioAtencionF():
    respuesta = promedio_atencion()
    return respuesta,200

#contar 
@app.get("/cantidadReservacion")
def cantidadReservacion():
    respuesta = suma_cantidad_mes_anioByEspecialidad()
    return respuesta,200


