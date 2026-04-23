from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models 
import schemas
from database import SessionLocal, engine
import predictor 
print("--- DEBUG PREDICTOR ---")
print(f"Archivo cargado desde: {predictor.__file__}")
print(f"¿Tiene UMBRAL_ETAPA1?: {'UMBRAL_ETAPA1' in dir(predictor)}")
print(f"Atributos: {dir(predictor)}")
print("-----------------------")
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
        
        # Detección de etapa
        es_etapa2 = datos_ia.get("creatinina") is not None and float(datos_ia.get("creatinina")) > 0
        etapa_a_usar = 2 if es_etapa2 else 1
        
        probabilidad = predictor.ejecutar_prediccion(datos_ia, etapa=etapa_a_usar)
        
        # Aplicación de umbrales específicos
        umbral = predictor.UMBRAL_ETAPA2 if etapa_a_usar == 2 else predictor.UMBRAL_ETAPA1
        riesgo_label = "Alto" if probabilidad >= umbral else "Bajo"
        
        return {
            "probabilidad": probabilidad,
            "riesgo": riesgo_label, 
            "etapa_aplicada": etapa_a_usar,
            "umbral_aplicado": umbral
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@app.post("/pacientes/", response_model=schemas.Paciente)
def guardar_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    datos_dict = paciente.model_dump()
    datos_ia = {k: v for k, v in datos_dict.items() if k not in ["fecha_creacion", "fecha_actualizacion", "id"]}
    
    etapa = 2 if datos_ia.get("creatinina") else 1
    score_ia = predictor.ejecutar_prediccion(datos_ia, etapa=etapa)

    nuevo_paciente = models.Paciente(**datos_dict)
    
    if etapa == 1:
        nuevo_paciente.riesgo_preliminar = score_ia
    else:
        nuevo_paciente.riesgo_final = score_ia
    
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
    paciente_db = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente_db:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    datos_dict = datos_actualizados.model_dump()
    datos_ia = {k: v for k, v in datos_dict.items() if k not in ["fecha_creacion", "fecha_actualizacion", "id"]}
    
    etapa = 2 if datos_ia.get("creatinina") else 1
    nuevo_score_ia = predictor.ejecutar_prediccion(datos_ia, etapa=etapa)

    for key, value in datos_dict.items():
        if key not in ["fecha_creacion", "id"]:
            setattr(paciente_db, key, value)
    

    if etapa == 1:
        paciente_db.riesgo_preliminar = nuevo_score_ia
    else:
        paciente_db.riesgo_final = nuevo_score_ia
    
    paciente_db.probabilidad_riesgo = nuevo_score_ia

    try:
        db.commit()
        db.refresh(paciente_db)
        return paciente_db
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar")
    
    
@app.get("/pacientes/", response_model=list[schemas.Paciente])
def obtener_pacientes(top: int = None, db: Session = Depends(get_db)):
    """
    Trae la lista de pacientes. 
    Uso: /pacientes/ (trae todos) o /pacientes/?top=10 (trae los primeros 10)
    """
    query = db.query(models.Paciente).order_by(models.Paciente.id.desc())
    
    if top:
        return query.limit(top).all()
    
    return query.all()