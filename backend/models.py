from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    # Identificación única en la base de datos
    id = Column(Integer, primary_key=True, index=True)
    
    # Fechas
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Datos de identificación del paciente
    dni = Column(String, unique=True, index=True)
    nombre = Column(String)
    apellido = Column(String)
    
    edad = Column(Float)
    genero = Column(Float) 
    fumo_100_cigarrillos = Column(Float) 
    consumo_alcohol_ultimo_año = Column(Float)
    actividad_deportiva_moderada_x_semana = Column(Float)
    anhedonia = Column(Float)
    peso = Column(Float)
    altura = Column(Float)
    bmi = Column(Float)
    presion_sistolica_final = Column(Float)
    presion_diastolica_final = Column(Float)
    
    # Antecedentes
    fam_cardio = Column(Float)
    fam_diabetes = Column(Float)
    fam_asma = Column(Float)
    riñones_debiles_fallando = Column(Float)
    hipertension = Column(Float)
    diabetes = Column(Float)
    
    # Valores de Laboratorio
    colesterol_total = Column(Float)
    hdl = Column(Float)
    trigliceridos = Column(Float)
    proteina_c = Column(Float)
    hemoglobina = Column(Float)
    creatinina = Column(Float)
    acido_urico = Column(Float)
    potasio = Column(Float)

    # Para guardar el resultado final de la IA
    probabilidad_riesgo = Column(Float, nullable=True)