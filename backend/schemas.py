from pydantic import BaseModel
from typing import Optional

# Esta clase define qué datos necesitamos recibir del frontend
class PacienteBase(BaseModel):
    dni: str
    nombre: str
    apellido: str
    edad: float
    genero: str
    fumo_100_cigarrillos: str
    consumo_alcohol_ultimo_año: float
    actividad_deportiva_moderada_x_semana: float
    anhedonia: float
    bmi: float
    presion_sistolica_final: float
    presion_diastolica_final: float
    fam_cardio: float
    fam_diabetes: float
    fam_asma: float
    riñones_debiles_fallando: float
    hipertension: float
    diabetes: float
    colesterol_total: float
    hdl: float
    trigliceridos: float
    proteina_c: float
    hemoglobina: float
    creatinina: float
    acido_urico: float
    potasio: float

# Esto se usa cuando creamos un paciente (es igual al anterior)
class PacienteCreate(PacienteBase):
    pass

# Esto es lo que el servidor devuelve (incluye el ID y el resultado de la IA)
class Paciente(PacienteBase):
    id: int
    probabilidad_riesgo: Optional[float] = None

    class Config:
        from_attributes = True