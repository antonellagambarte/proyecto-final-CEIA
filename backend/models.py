from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    dni = Column(String, unique=True, index=True) # El DNI es único para la persona
    nombre = Column(String)
    apellido = Column(String)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    
    # Un paciente tiene muchas visitas
    visitas = relationship("Visita", back_populates="paciente")

class Visita(Base):
    __tablename__ = "visitas"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    fecha_visita = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())

    # Movemos todos los datos clínicos aquí
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
    
    fam_cardio = Column(Float)
    fam_diabetes = Column(Float)
    fam_asma = Column(Float)
    riñones_debiles_fallando = Column(Float)
    hipertension = Column(Float)
    diabetes = Column(Float)
    asma = Column(Float)
    
    colesterol_total = Column(Float)
    hdl = Column(Float)
    trigliceridos = Column(Float)
    proteina_c = Column(Float)
    hemoglobina = Column(Float)
    creatinina = Column(Float)
    acido_urico = Column(Float)
    potasio = Column(Float)

    riesgo_preliminar = Column(Float, nullable=True) 
    riesgo_final = Column(Float, nullable=True)     
    probabilidad_riesgo = Column(Float, nullable=True)

    paciente = relationship("Paciente", back_populates="visitas")