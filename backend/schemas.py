from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class VisitaBase(BaseModel):
    fecha_nacimiento: Optional[str] = None
    edad: Optional[float] = None
    genero: Optional[float] = None 
    fumo_100_cigarrillos: Optional[float] = None
    consumo_alcohol_ultimo_año: Optional[float] = 0.0
    actividad_deportiva_moderada_x_semana: Optional[float] = 0.0
    anhedonia: Optional[float] = 0.0
    bmi: Optional[float] = None 
    peso: Optional[float] = None
    altura: Optional[float] = None
    presion_sistolica_final: Optional[float] = None
    presion_diastolica_final: Optional[float] = None
    fam_cardio: Optional[float] = None
    fam_diabetes: Optional[float] = None
    fam_asma: Optional[float] = None
    riñones_debiles_fallando: Optional[float] = None
    hipertension: Optional[float] = None
    diabetes: Optional[float] = None
    asma: Optional[float] = None
    colesterol_total: Optional[float] = None
    hdl: Optional[float] = None
    trigliceridos: Optional[float] = None
    proteina_c: Optional[float] = None
    hemoglobina: Optional[float] = None
    creatinina: Optional[float] = None
    acido_urico: Optional[float] = None
    potasio: Optional[float] = None

# 2. Esquema para la tabla de Visitas
class Visita(VisitaBase):
    id: int
    paciente_id: int
    fecha_visita: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    riesgo_preliminar: Optional[float] = None
    riesgo_final: Optional[float] = None
    probabilidad_riesgo: Optional[float] = None
    base_value_preliminar: Optional[float] = None
    base_value_final: Optional[float] = None
    

    class Config:
        from_attributes = True

class PacienteCreate(VisitaBase):
    dni: str
    nombre: str
    apellido: str


class Paciente(BaseModel):
    id: int
    dni: str
    nombre: str
    apellido: str
    fecha_creacion: Optional[datetime] = None
    visitas: List[Visita] = [] 

    class Config:
        from_attributes = True