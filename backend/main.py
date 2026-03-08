from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models 
import schemas
from database import SessionLocal, engine
import predictor 

# Crear las tablas en el archivo SQLite
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CardioPredict API - SQLite Version")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- RUTAS ---

@app.get("/")
def home():
    return {"message": "Backend CardioPredict activo con SQLite"}

@app.post("/pacientes/predecir")
def predecir_al_vuelo(datos: dict):
    try:
        datos_ia = {k: v for k, v in datos.items() if k not in ["fecha_creacion", "fecha_actualizacion", "id"]}
        etapa_a_usar = 2 if datos_ia.get("creatinina") else 1
        probabilidad = predictor.ejecutar_prediccion(datos_ia, etapa=etapa_a_usar)
        
        return {
            "probabilidad": probabilidad,
            "riesgo": "Alto" if probabilidad > 0.5 else "Bajo",
            "etapa_aplicada": etapa_a_usar
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al procesar la predicción")

@app.post("/pacientes/", response_model=schemas.Paciente)
def guardar_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    """
    Confirmación: Guarda al paciente en el archivo .db e incluye el score.
    """
    datos_dict = paciente.model_dump()
    
    datos_ia = {k: v for k, v in datos_dict.items() if k not in ["fecha_creacion", "fecha_actualizacion", "id"]}
    etapa = 2 if datos_ia.get("creatinina") is not None else 1
    score_ia = predictor.ejecutar_prediccion(datos_ia, etapa=etapa)

    nuevo_paciente = models.Paciente(**datos_dict)
    nuevo_paciente.probabilidad_riesgo = score_ia
    
    try:
        db.add(nuevo_paciente)
        db.commit()
        db.refresh(nuevo_paciente)
        return nuevo_paciente
    except Exception as e:
        db.rollback()
        print(f"Error al guardar: {e}")
        raise HTTPException(status_code=500, detail="No se pudo guardar")

@app.get("/pacientes/buscar/{dni_parcial}", response_model=list[schemas.Paciente])
def buscar_pacientes_por_dni(dni_parcial: str, db: Session = Depends(get_db)):
    return db.query(models.Paciente).filter(models.Paciente.dni.contains(dni_parcial)).all()

@app.put("/pacientes/{paciente_id}", response_model=schemas.Paciente)
def actualizar_paciente(paciente_id: int, datos_actualizados: schemas.PacienteCreate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un paciente existente y recalcula el riesgo automáticamente.
    """
    paciente_db = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente_db:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    datos_dict = datos_actualizados.model_dump()

    datos_ia = {k: v for k, v in datos_dict.items() if k not in ["fecha_creacion", "fecha_actualizacion", "id"]}
    etapa = 2 if datos_ia.get("creatinina") is not None else 1
    nuevo_score_ia = predictor.ejecutar_prediccion(datos_ia, etapa=etapa)


    for key, value in datos_dict.items():
        if key not in ["fecha_creacion", "id"]:
            setattr(paciente_db, key, value)
    
    paciente_db.probabilidad_riesgo = nuevo_score_ia

    try:
        db.commit()
        db.refresh(paciente_db)
        return paciente_db
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar")