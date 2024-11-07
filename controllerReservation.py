import pandas as pd
from sqlalchemy.orm import Session
from db import get_db
from models import Usuario, Reservacion
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import json

class UsuarioResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class ReservacionResponse(BaseModel):
    id: int
    doctor_name: str
    especialidad: str
    paciente_name: str
    paciente_last_name: str
    paciente_address: str
    paciente_sexo: str
    fecha_reservado: Optional[date]
    fecha_cancelado: Optional[date]
    fecha_atendido: Optional[date]
    stado_state: str
    cantidad: int
    tiempo_atencion: int
    cantida_anticipacion: int
    costo: float

    class Config:
        from_attributes = True

def get_all_users(db: Session):
    """Fetch all users from the database."""
    try:
        return db.query(Usuario).all()
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []

def get_all_reservacion(db: Session):
    """Fetch all reservations from the database."""
    try:
        return db.query(Reservacion).all()
    except Exception as e:
        print(f"Error fetching reservations: {e}")
        return []

def promedio_atencion(data):
    """Calculate the average attention time for a given specialty."""
    try:
        df = data_frame()
        especialidad = data.get("especialidad")
        df_filtrado = df[df["especialidad"] == especialidad]

        promedio = df_filtrado["tiempo_atencion"].mean() if not df_filtrado.empty else None
        respuesta = {
            "Promedio": promedio,
            "Mensaje": "No hay datos disponibles para esta especialidad" if promedio is None else "Promedio calculado con éxito",
            "res": "true"
        }
        return respuesta
    except Exception as e:
        print(f"Error calculating average attention time: {e}")
        return {"error": "No se pudo calcular el promedio"}

def suma_ingreso_mes_anio():
    """Calculate the sum of income by month and year."""
    try:
        df = data_frame()
        df['fecha_atendido'] = pd.to_datetime(df['fecha_atendido'])
        suma_costo_por_anio_mes = df.groupby([df['fecha_atendido'].dt.year, df['fecha_atendido'].dt.month])['costo'].sum()
        suma_costo_por_anio_mes = suma_costo_por_anio_mes.unstack(level=1)
        return suma_costo_por_anio_mes.to_json(orient='index')
    except Exception as e:
        print(f"Error calculating income sum: {e}")
        return json.dumps({"error": "No se pudo calcular la suma de ingresos"})

def suma_ingreso_mes_anioByEspecialidad(especialidad):
    """Calculate the sum of income by month and year, filtered by specialty."""
    try:
        df = data_frame()
        df['fecha_atendido'] = pd.to_datetime(df['fecha_atendido'])
        df_especialidad = df[df['especialidad'] == especialidad] if especialidad else df
        suma_costo_por_anio_mes = df_especialidad.groupby([df['fecha_atendido'].dt.year, df['fecha_atendido'].dt.month])['costo'].sum()
        suma_costo_por_anio_mes = suma_costo_por_anio_mes.unstack(level=1)
        return suma_costo_por_anio_mes.to_json(orient='index')
    except Exception as e:
        print(f"Error calculating income sum by specialty: {e}")
        return json.dumps({"error": "No se pudo calcular la suma de ingresos por especialidad"})

def suma_cantidad_mes_anioByEspecialidad(especialidad=''):
    """Calculate the sum of quantities by month and year, filtered by specialty."""
    try:
        df = data_frame()
        df['fecha_atendido'] = pd.to_datetime(df['fecha_atendido'])
        df_especialidad = df[df['especialidad'] == especialidad] if especialidad else df
        suma_cantidad_por_anio_mes = df_especialidad.groupby([df['fecha_atendido'].dt.year, df['fecha_atendido'].dt.month])['cantidad'].sum()
        suma_cantidad_por_anio_mes = suma_cantidad_por_anio_mes.unstack(level=1)
        return suma_cantidad_por_anio_mes.to_json(orient='index')
    except Exception as e:
        print(f"Error calculating quantity sum by specialty: {e}")
        return json.dumps({"error": "No se pudo calcular la cantidad de reservas por especialidad"})

def promedio_atencion():
    """Calculate the average attention time for each specialty."""
    try:
        df = data_frame()
        promedio_tiempo_atencion = df.groupby('especialidad')['tiempo_atencion'].mean().reset_index()
        return promedio_tiempo_atencion.to_json(orient='records')
    except Exception as e:
        print(f"Error calculating average attention time: {e}")
        return json.dumps({"error": "No se pudo calcular el promedio de atención"})

def promedio_atencionM():
    """Calculate the average attention time for male patients for each specialty."""
    try:
        df = data_frame()
        df_masculino = df[df['paciente_sexo'] == 'M']
        promedio_tiempo_atencion = df_masculino.groupby('especialidad')['tiempo_atencion'].mean().reset_index()
        return promedio_tiempo_atencion.to_json(orient='records')
    except Exception as e:
        print(f"Error calculating average attention time for male patients: {e}")
        return json.dumps({"error": "No se pudo calcular el promedio de atención para hombres"})

def promedio_atencionF():
    """Calculate the average attention time for female patients for each specialty."""
    try:
        df = data_frame()
        df_femenino = df[df['paciente_sexo'] == 'F']
        promedio_tiempo_atencion = df_femenino.groupby('especialidad')['tiempo_atencion'].mean().reset_index()
        return promedio_tiempo_atencion.to_json(orient='records')
    except Exception as e:
        print(f"Error calculating average attention time for female patients: {e}")
        return json.dumps({"error": "No se pudo calcular el promedio de atención para mujeres"})

def get_especialidades():
    """Retrieve all unique specialties from the data."""
    try:
        df = data_frame()
        especialidades_unicas = df['especialidad'].unique()
        return especialidades_unicas.tolist()
    except Exception as e:
        print(f"Error retrieving specialties: {e}")
        return json.dumps({"error": "No se pudieron obtener las especialidades"})

def cantidad():
    """Calculate the count of male and female patients."""
    try:
        reservacion_df = data_frame()
        reservacion_df["Genero"] = reservacion_df["paciente_sexo"].apply(lambda sexo: "M" if sexo == "M" else "F")
        hombres = reservacion_df[reservacion_df["Genero"] == "M"].shape[0]
        mujeres = reservacion_df[reservacion_df["Genero"] == "F"].shape[0]

        return {"hombres": hombres, "mujeres": mujeres}
    except Exception as e:
        print(f"Error calculating patient count by gender: {e}")
        return json.dumps({"error": "No se pudo calcular el conteo de pacientes por género"})

def fetch_all_users():
    """Fetch all users from the database and convert them to Pydantic models."""
    db = next(get_db())
    try:
        users = get_all_users(db)
        return [UsuarioResponse.from_orm(user).dict() for user in users]
    except Exception as e:
        print(f"Error fetching all users: {e}")
        return []
    finally:
        db.close()

def fetch_all_reservacion():
    """Fetch all reservations from the database and convert them to Pydantic models."""
    db = next(get_db())
    try:
        reservacion = get_all_reservacion(db)
        return [ReservacionResponse.from_orm(res).dict() for res in reservacion]
    except Exception as e:
        print(f"Error fetching all reservations: {e}")
        return []
    finally:
        db.close()

def data_frame():
    """Retrieve all reservations and convert them to a DataFrame for further processing."""
    try:
        reservacion_response = fetch_all_reservacion()
        return pd.DataFrame(reservacion_response)
    except Exception as e:
        print(f"Error converting reservations to DataFrame: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of failure
