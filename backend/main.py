from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models 
import schemas
from database import SessionLocal, engine
import predictor # Tu lógica de CatBoost

# Crear las tablas en el archivo SQLite (sql_app.db)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CardioPredict API - SQLite Version")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para la base de datos SQLite
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

# RUTA PARA EL BOTÓN "PREDECIR" 
@app.post("/pacientes/predecir")
def predecir_al_vuelo(datos: dict):
    """
    Simulador: El médico puede probar valores infinitas veces.
    NO guarda nada en la base de datos.
    """
    try:
        # Detectar si es etapa 1 o 2 para el modelo
        etapa_a_usar = 2 if datos.get("creatinina") else 1
        
        probabilidad = predictor.ejecutar_prediccion(datos, etapa=etapa_a_usar)
        
        return {
            "probabilidad": probabilidad,
            "riesgo": "Alto" if probabilidad > 0.5 else "Bajo",
            "etapa_aplicada": etapa_a_usar
        }
    except Exception as e:
        print(f"Error en simulación: {e}")
        raise HTTPException(status_code=500, detail="Error al procesar la predicción")

# RUTA PARA EL BOTÓN "GUARDAR" 
@app.post("/pacientes/", response_model=schemas.Paciente)
def guardar_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    """
    Confirmación: Guarda al paciente en el archivo .db e incluye el score.
    """
    datos_dict = paciente.model_dump()
    
    # Recalculamos la predicción final para asegurar el dato antes de guardar
    etapa = 2 if datos_dict.get("creatinina") is not None else 1
    score_ia = predictor.ejecutar_prediccion(datos_dict, etapa=etapa)

    # Mapeo al modelo de base de datos
    nuevo_paciente = models.Paciente(**datos_dict)
    nuevo_paciente.probabilidad_riesgo = score_ia
    
    try:
        db.add(nuevo_paciente)
        db.commit()
        db.refresh(nuevo_paciente)
        return nuevo_paciente
    except Exception as e:
        db.rollback()
        print(f"Error al guardar en SQLite: {e}")
        raise HTTPException(status_code=500, detail="No se pudo guardar en la base de datos")

@app.get("/pacientes/buscar/{dni_parcial}", response_model=list[schemas.Paciente])
def buscar_pacientes_por_dni(dni_parcial: str, db: Session = Depends(get_db)):
    # busca cualquier DNI que tenga esa cadena de números
    pacientes = db.query(models.Paciente).filter(models.Paciente.dni.contains(dni_parcial)).all()
    
    # Si no encuentra ninguno, devolvemos lista vacía
    return pacientes

@app.put("/pacientes/{paciente_id}", response_model=schemas.Paciente)
def actualizar_paciente(paciente_id: int, datos_actualizados: schemas.PacienteCreate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un paciente existente y recalcula el riesgo automáticamente.
    """
    paciente_db = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not paciente_db:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    datos_dict = datos_actualizados.model_dump()

    etapa = 2 if datos_dict.get("creatinina") is not None else 1
    nuevo_score_ia = predictor.ejecutar_prediccion(datos_dict, etapa=etapa)

    for key, value in datos_dict.items():
        setattr(paciente_db, key, value)
    
    paciente_db.probabilidad_riesgo = nuevo_score_ia

    try:
        db.commit()
        db.refresh(paciente_db)
        return paciente_db
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar los datos en la base de datos")