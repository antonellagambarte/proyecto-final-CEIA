from pydantic import BaseModel
from typing import Optional

class PacienteBase(BaseModel):
    dni: str
    nombre: str
    apellido: str
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
    colesterol_total: Optional[float] = None
    hdl: Optional[float] = None
    trigliceridos: Optional[float] = None
    proteina_c: Optional[float] = None
    hemoglobina: Optional[float] = None
    creatinina: Optional[float] = None
    acido_urico: Optional[float] = None
    potasio: Optional[float] = None

class PacienteCreate(PacienteBase):
    pass

class Paciente(PacienteBase):
    id: int
    probabilidad_riesgo: Optional[float] = None

    class Config:
        from_attributes = True