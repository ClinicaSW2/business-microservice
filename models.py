from sqlalchemy import Column, Integer, String, Date, Float, CHAR,true
from db import Base,engine

class Usuario(Base):
    __tablename__ = "usuarios"
    id =Column(Integer,autoincrement=true,primary_key=true)
    username=Column(String(70),unique=true)
    password = Column(String(40))

class Reservacion(Base):
    __tablename__ = "reservacion"
    id =Column(Integer,autoincrement=true,primary_key=true)
    doctor_name = Column(String(100))
    especialidad = Column(String(50))
    paciente_name = Column(String(100))
    paciente_last_name = Column(String(100))
    paciente_address = Column(String(200))
    paciente_sexo = Column(CHAR(1))
    fecha_reservado = Column(Date)
    fecha_cancelado = Column(Date)
    fecha_atendido = Column(Date)
    stado_state = Column(String(30))
    cantidad = Column(Integer)
    tiempo_atencion = Column(Integer)
    cantida_anticipacion = Column(Integer)
    costo = Column(Float)

Base.metadata.create_all(engine)