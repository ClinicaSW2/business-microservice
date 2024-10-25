import pandas as pd
from sqlalchemy.orm import Session
from db import get_db
from models import Usuario,Reservacion
from pydantic import BaseModel
from typing import List
from datetime import date
from typing import Optional
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
    return db.query(Usuario).all()

def get_all_reservacion(db: Session):
    return db.query(Reservacion).all()

def promedio_atencion(data):
    df = data_frame()
    especialidad = data.get("especialidad")

    df_filtrado = df[df["especialidad"]== especialidad]

    if not df_filtrado.empty:
        promedio = df_filtrado["tiempo_atencion"].mean()
    else:
        promedio = None
    print(especialidad )

    respuesta = {
        "Promedio": promedio,
        "Mensaje": "No hay datos disponibles para esta especialidad" if promedio is None else "Promedio calculado con éxito",
        "res": "true"
    }
    return respuesta

def suma_ingreso_mes_anio():
    try:
        df = data_frame()
        df['fecha_atendido'] = pd.to_datetime(df['fecha_atendido'])
        suma_costo_por_anio_mes = df.groupby([df['fecha_atendido'].dt.year, df['fecha_atendido'].dt.month])['costo'].sum()
        suma_costo_por_anio_mes = suma_costo_por_anio_mes.unstack(level=1)
        suma_costo_por_anio_mes_json = suma_costo_por_anio_mes.to_json(orient='index')
        return suma_costo_por_anio_mes_json
    except Exception as e:
        print("Error al exportar el archivo JSON:", e)
        return None
    
def suma_ingreso_mes_anioByEspecialidad(especialidad):
    try:
        df = data_frame()
        df['fecha_atendido'] = pd.to_datetime(df['fecha_atendido'])
        if especialidad != '':          
            df_especialidad = df[df['especialidad'] == especialidad]
            suma_costo_por_anio_mes = df_especialidad.groupby([df['fecha_atendido'].dt.year, df['fecha_atendido'].dt.month])['costo'].sum()
        else:
            suma_costo_por_anio_mes = df.groupby([df['fecha_atendido'].dt.year, df['fecha_atendido'].dt.month])['costo'].sum()
        suma_costo_por_anio_mes = suma_costo_por_anio_mes.unstack(level=1)
        suma_costo_por_anio_mes_json = suma_costo_por_anio_mes.to_json(orient='index')
         
        return suma_costo_por_anio_mes_json
    except Exception as e:
        print("Error al exportar el archivo JSON:", e)
        return None
    

def suma_cantidad_mes_anioByEspecialidad(especialidad=''):
    try:
        df = data_frame()
        df['fecha_atendido'] = pd.to_datetime(df['fecha_atendido'])
        
        if especialidad:
            df_especialidad = df[df['especialidad'] == especialidad]
            suma_cantidad_por_anio_mes = df_especialidad.groupby([df_especialidad['fecha_atendido'].dt.year, df_especialidad['fecha_atendido'].dt.month])['cantidad'].sum()
        else:
            suma_cantidad_por_anio_mes = df.groupby([df['fecha_atendido'].dt.year, df['fecha_atendido'].dt.month])['cantidad'].sum()
        
        suma_cantidad_por_anio_mes = suma_cantidad_por_anio_mes.unstack(level=1)
        suma_cantidad_por_anio_mes_json = suma_cantidad_por_anio_mes.to_json(orient='index')
        
        return suma_cantidad_por_anio_mes_json
    except Exception as e:
        print("Error al exportar el archivo JSON:", e)
        return None
    



def promedio_atencion():
    df = data_frame()
    promedio_tiempo_atencion = df.groupby('especialidad')['tiempo_atencion'].mean().reset_index()
    promedio_tiempo_atencion.columns = ['especialidad', 'promedio_tiempo_atencion']
    
    # Convertir el DataFrame a JSON
    resultado_dict = promedio_tiempo_atencion.to_dict(orient='records')
    resultado_json = json.dumps(resultado_dict, ensure_ascii=False, indent=4)
    
    return resultado_json

def promedio_atencionM():
    df = data_frame()
    df_masculino = df[df['paciente_sexo'] == 'M']
    promedio_tiempo_atencion = df_masculino.groupby('especialidad')['tiempo_atencion'].mean().reset_index()
    promedio_tiempo_atencion.columns = ['especialidad', 'promedio_tiempo_atencion']
    resultado_dict = promedio_tiempo_atencion.to_dict(orient='records')
    resultado_json = json.dumps(resultado_dict, ensure_ascii=False, indent=4)
    
    return resultado_json


def promedio_atencionF():
    df = data_frame()
    promedio_tiempo_atencion = df.groupby('especialidad')['tiempo_atencion'].mean().reset_index()
    promedio_tiempo_atencion.columns = ['especialidad', 'promedio_tiempo_atencion']
    
    # Convertir el DataFrame a JSON
    resultado_dict = promedio_tiempo_atencion.to_dict(orient='records')
    resultado_json = json.dumps(resultado_dict, ensure_ascii=False, indent=4)
    
    return resultado_json


def get_especialidades():
    try:
        df = data_frame() 
        especialidades_unicas = df['especialidad'].unique()
        return especialidades_unicas.tolist()
    except Exception as e:
        print("Error al obtener especialidades:", e)
        return None



def cantidad():
    reservacion_df = data_frame()
    reservacion_df["Genero"] = reservacion_df["paciente_sexo"].apply(lambda nombre: "M" if nombre.endswith("F") else "F")
    hombres = reservacion_df[reservacion_df["Genero"] == "M"].shape[0]
    mujeres = reservacion_df[reservacion_df["Genero"] == "F"].shape[0]

    respuesta = {
        "hombres": hombres,
        "mujeres": mujeres
    }
    return respuesta







def fetch_all_users():
    db = next(get_db())
    try:
        users = get_all_users(db)
        users_response = [UsuarioResponse.from_orm(user).dict() for user in users]
        return users_response
    finally:
        db.close()

def fetch_all_reservacion():
    db = next(get_db())
    try:
        reservacion = get_all_reservacion(db)
        reservacion_response = [ReservacionResponse.from_orm(res).dict() for res in reservacion]
        return reservacion_response
    finally:
        db.close()

def data_frame():
    reservacion_response = fetch_all_reservacion()
    # Configuración para mostrar todas las filas y columnas sin truncar
    # pd.set_option('display.max_rows', None)  # Mostrar todas las filas
    # pd.set_option('display.max_columns', None)  # Mostrar todas las columnas
    # pd.set_option('display.width', None)  # No truncar el ancho de las columnas
    # Imprimir el DataFrame completo
    #print(reservacion_response)
    return pd.DataFrame(reservacion_response)