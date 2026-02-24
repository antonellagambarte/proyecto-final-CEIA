from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models 
import schemas
from database import SessionLocal, engine
import predictor

# Usamos los modelos definidos en models.py para crear las tablas en Postgres
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ESTA ES LA FUNCIÓN QUE TE FALTABA
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "API de CardioPredict conectada a la base de datos"}

@app.get("/pacientes/{dni}", response_model=schemas.Paciente)
def obtener_paciente(dni: str, db: Session = Depends(get_db)):
    paciente = db.query(models.Paciente).filter(models.Paciente.dni == dni).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente

import predictor  # Importante: asegurate de que el archivo predictor.py esté en la misma carpeta

@app.post("/pacientes/", response_model=schemas.Paciente)
def crear_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    # 1. Convertimos los datos que vienen del frontend a un diccionario
    datos_dict = paciente.model_dump()
    
    # 2. Decidimos qué etapa usar (Lógica de negocio)
    # Si el médico cargó datos clínicos (etapa 2), usamos el modelo 2.
    # Si solo hay datos básicos, usamos etapa 1.
    # (Usamos la creatinina como "indicador" de que es etapa 2)
    etapa_a_usar = 2 if datos_dict.get("creatinina") is not None else 1
    
    # 3. Llamamos a la IA para obtener la probabilidad
    try:
        score_ia = predictor.ejecutar_prediccion(datos_dict, etapa=etapa_a_usar)
    except Exception as e:
        # Si la IA falla, podemos guardar el error o poner un valor por defecto
        print(f"Error en la predicción: {e}")
        score_ia = 0.0

    # 4. Creamos el registro para la base de datos
    nuevo_paciente = models.Paciente(**datos_dict)
    nuevo_paciente.probabilidad_riesgo = score_ia
    
    # 5. Guardar en PostgreSQL
    db.add(nuevo_paciente)
    db.commit()
    db.refresh(nuevo_paciente)
    
    return nuevo_paciente