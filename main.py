from flask import Flask, jsonify, request
from sqlalchemy.orm import Session
from controllerReservation import (
    fetch_all_users, fetch_all_reservacion, promedio_atencion,
    suma_ingreso_mes_anio, suma_ingreso_mes_anioByEspecialidad,
    get_especialidades, suma_cantidad_mes_anioByEspecialidad,
    promedio_atencionF, promedio_atencionM
)
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Esto permite solicitudes CORS desde cualquier origen

@app.route("/users", methods=["GET"])
def read_users():
    """
    Endpoint para obtener todos los usuarios.
    
    Retorna:
        JSON con la lista de usuarios o un mensaje de error en caso de excepción.
    """
    try:
        users_response = fetch_all_users()
        return jsonify(users_response), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener los usuarios", "details": str(e)}), 500

@app.route("/powerBI", methods=["GET"])
def read_reservacion():
    """
    Endpoint para obtener todas las reservaciones.
    
    Retorna:
        JSON con la lista de reservaciones o un mensaje de error en caso de excepción.
    """
    try:
        reservacion_response = fetch_all_reservacion()
        return jsonify(reservacion_response), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener las reservaciones", "details": str(e)}), 500

@app.route("/promedioatencion", methods=["GET"])
def get_promedio_atencion():
    """
    Endpoint para obtener el promedio de atención.
    Espera un JSON en el cuerpo de la solicitud con los datos necesarios.
    
    Retorna:
        JSON con el promedio de atención o un mensaje de error en caso de excepción.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Falta el cuerpo de la solicitud JSON"}), 400
    try:
        respuesta = promedio_atencion(data)
        return jsonify(respuesta), 200
    except Exception as e:
        return jsonify({"error": "Error al calcular el promedio de atención", "details": str(e)}), 500

@app.route("/", methods=["GET"])
def hello_world():
    """
    Endpoint básico de prueba para verificar que el servidor esté en funcionamiento.
    
    Retorna:
        JSON con un mensaje de éxito.
    """
    return jsonify({"res": "true", "message": "todo ok!"}), 200

@app.route("/user", methods=["GET"])
def getUsers():
    """
    Endpoint para obtener un mensaje de prueba relacionado con los usuarios.
    
    Retorna:
        JSON con un mensaje de éxito.
    """
    return jsonify({"Users": "Todos los usuarios están aquí"}), 200

@app.route("/sumaingresobymesbyanio", methods=["GET"])
def get_suma_ingreso_mes_anio():
    """
    Endpoint para obtener la suma de ingresos por mes y año.
    
    Retorna:
        JSON con la suma de ingresos o un mensaje de error en caso de excepción.
    """
    try:
        respuesta = suma_ingreso_mes_anio()
        return jsonify(respuesta), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener la suma de ingresos por mes y año", "details": str(e)}), 500

@app.route("/sumaingresobymesbyanioByEspecialidad", methods=["GET"])
def get_suma_ingreso_mes_anioFilEspecilidad():
    """
    Endpoint para obtener la suma de ingresos por mes y año, filtrado por especialidad.
    Requiere el parámetro 'especialidad' en la URL.
    
    Retorna:
        JSON con la suma de ingresos filtrada por especialidad o un mensaje de error en caso de excepción.
    """
    especialidad = request.args.get('especialidad')
    # if not especialidad:
    #     return jsonify({"error": "Parámetro 'especialidad' es requerido"}), 400
    try:
        respuesta = suma_ingreso_mes_anioByEspecialidad(especialidad)
        return jsonify(respuesta), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener la suma de ingresos por especialidad", "details": str(e)}), 500

@app.route("/getespecialidad", methods=["GET"])
def get_especialidad():
    """
    Endpoint para obtener todas las especialidades existentes.
    
    Retorna:
        JSON con la lista de especialidades o un mensaje de error en caso de excepción.
    """
    try:
        respuesta = get_especialidades()
        return jsonify(respuesta), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener las especialidades", "details": str(e)}), 500

@app.route("/promedioAtencion", methods=["GET"])
def promedioAtencion():
    """
    Endpoint para obtener el promedio de atención general.
    
    Retorna:
        JSON con el promedio de atención o un mensaje de error en caso de excepción.
    """
    try:
        respuesta = promedio_atencion()
        return jsonify(respuesta), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener el promedio de atención", "details": str(e)}), 500

@app.route("/promedioAtencionM", methods=["GET"])
def promedioAtencionM():
    """
    Endpoint para obtener el promedio de atención para hombres.
    
    Retorna:
        JSON con el promedio de atención para hombres o un mensaje de error en caso de excepción.
    """
    try:
        respuesta = promedio_atencionM()
        return jsonify(respuesta), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener el promedio de atención para hombres", "details": str(e)}), 500

@app.route("/promedioAtencionF", methods=["GET"])
def promedioAtencionF():
    """
    Endpoint para obtener el promedio de atención para mujeres.
    
    Retorna:
        JSON con el promedio de atención para mujeres o un mensaje de error en caso de excepción.
    """
    try:
        respuesta = promedio_atencionF()
        return jsonify(respuesta), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener el promedio de atención para mujeres", "details": str(e)}), 500

@app.route("/cantidadReservacion", methods=["GET"])
def cantidadReservacion():
    """
    Endpoint para obtener la cantidad de reservaciones, filtrado por especialidad.
    
    Retorna:
        JSON con la cantidad de reservaciones o un mensaje de error en caso de excepción.
    """
    try:
        respuesta = suma_cantidad_mes_anioByEspecialidad()
        return jsonify(respuesta), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener la cantidad de reservaciones por especialidad", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
