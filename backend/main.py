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
    return {"message": "Backend CardioPredict activo con SQLite (Relacional Visitas)"}

@app.post("/pacientes/predecir")
def predecir_al_vuelo(datos: dict):
    try:
        # MAPEO: Traducimos del lenguaje del Front al lenguaje del Modelo
        datos_ia = {
            "edad": datos.get("edad"),
            "genero": datos.get("genero"),
            "fumo_100_cigarrillos": datos.get("fumo_100_cigarrillos"),
            "consumo_alcohol_ultimo_año": datos.get("consumo_alcohol_ultimo_año"),
            "actividad_deportiva_moderada_x_semana": datos.get("actividad_deportiva_moderada_x_semana"),
            "anhedonia": datos.get("anhedonia"),
            "peso": datos.get("peso"),
            "altura": datos.get("altura"),
            # Aquí corregimos los nombres:
            "presion_sistolica_final": datos.get("presion_sistolica_final"),
            "presion_diastolica_final": datos.get("presion_diastolica_final"),
            "colesterol_total": datos.get("colesterol_total"), # El front ya manda este nombre
            "hdl": datos.get("hdl"),
            "trigliceridos": datos.get("trigliceridos"),
            "proteina_c": datos.get("proteina_c"), # El front ya manda este nombre
            "creatinina": datos.get("creatinina"),
            "hipertension": datos.get("hipertension"),
            "diabetes": datos.get("diabetes"),
            "asma": datos.get("asma"),
            "riñones_debiles_fallando": datos.get("riñones_debiles_fallando"),
            "fam_cardio": datos.get("fam_cardio"),
            "fam_diabetes": datos.get("fam_diabetes"),
            "fam_asma": datos.get("fam_asma")
        }

        # Detección de etapa (mejorada)
        crea = datos.get("creatinina")
        etapa_a_usar = 2 if (crea is not None and str(crea).strip() != "" and float(crea) > 0) else 1
        
        # Llamada al predictor
        prob_calculada, influencias = predictor.ejecutar_prediccion(datos_ia, etapa=etapa_a_usar)
        
        # SÚPER IMPORTANTE: Casteo a float para evitar errores de serialización de NumPy
        prob_final = float(prob_calculada)

        return {
            "probabilidad": prob_final,
            "riesgo": "Alto" if prob_final >= 0.4 else "Bajo",
            "etapa_aplicada": etapa_a_usar,
            "influencias": influencias
        }
    except Exception as e:
        print(f"Error en endpoint predecir: {e}")
        return {"error": str(e), "probabilidad": 0}

@app.post("/pacientes/", response_model=schemas.Paciente)
def guardar_visita_paciente(paciente_in: schemas.PacienteCreate, db: Session = Depends(get_db)):
    datos_dict = paciente_in.model_dump()
    
    # 1. Ejecutar IA antes de tocar la DB
    etapa = 2 if datos_dict.get("creatinina") else 1
    datos_ia = {k: v for k, v in datos_dict.items() if k not in ["dni", "nombre", "apellido"]}
    
    score_ia_bruto, _ = predictor.ejecutar_prediccion(datos_ia, etapa=etapa)
    score_ia = float(score_ia_bruto) # Casteo a float estándar de Python

    try:
        paciente_db = db.query(models.Paciente).filter(models.Paciente.dni == datos_dict['dni']).first()
        
        if not paciente_db:
            paciente_db = models.Paciente(
                dni=datos_dict['dni'],
                nombre=datos_dict['nombre'],
                apellido=datos_dict['apellido']
            )
            db.add(paciente_db)
            db.commit()
            db.refresh(paciente_db)

        # 2. Crear la visita usando los datos filtrados
        nueva_visita = models.Visita(**datos_ia) 
        nueva_visita.paciente_id = paciente_db.id
        
        # Asignamos el score a los campos correspondientes
        nueva_visita.probabilidad_riesgo = score_ia
        if etapa == 1:
            nueva_visita.riesgo_preliminar = score_ia
        else:
            nueva_visita.riesgo_final = score_ia
        
        db.add(nueva_visita)
        db.commit()
        
        db.refresh(paciente_db)
        
        print(f">>> [DB SAVE] Guardado score: {score_ia} para paciente: {paciente_db.dni}")
        return paciente_db
        
    except Exception as e:
        db.rollback()
        print(f"Error al procesar visita: {e}")
        raise HTTPException(status_code=500, detail=f"Error al guardar: {e}")

@app.get("/pacientes/buscar/{dni_parcial}", response_model=list[schemas.Paciente])
def buscar_pacientes_por_dni(dni_parcial: str, db: Session = Depends(get_db)):
    # Buscamos en la tabla pacientes (datos fijos)
    return db.query(models.Paciente).filter(models.Paciente.dni.contains(dni_parcial)).all()

@app.get("/pacientes/", response_model=list[schemas.Paciente])
def obtener_pacientes(top: int = None, db: Session = Depends(get_db)):
    query = db.query(models.Paciente).order_by(models.Paciente.id.desc())
    if top:
        return query.limit(top).all()
    return query.all()

@app.get("/pacientes/{paciente_id}/visitas", response_model=list[schemas.Visita])
def obtener_historial_visitas(paciente_id: int, db: Session = Depends(get_db)):
    """
    Trae todas las consultas médicas de un paciente específico.
    """
    return db.query(models.Visita).filter(models.Visita.paciente_id == paciente_id).order_by(models.Visita.fecha_visita.desc()).all()

@app.put("/visitas/{visita_id}")
def actualizar_visita(visita_id: int, datos: dict, db: Session = Depends(get_db)):
    # 1. Buscar la visita existente
    visita_db = db.query(models.Visita).filter(models.Visita.id == visita_id).first()
    if not visita_db:
        raise HTTPException(status_code=404, detail="La visita no existe")

    try:
        # 2. Actualizar los campos que vienen del Front
        # Esto pisa los valores viejos (o nulls) con los nuevos (laboratorio, etc.)
        for key, value in datos.items():
            if hasattr(visita_db, key) and key not in ["id", "paciente_id", "fecha_visita"]:
                setattr(visita_db, key, value)

        # 3. Recalcular la IA con los nuevos datos
        # Ahora que tenemos laboratorio, la etapa será 2
        datos_ia = {
            "edad": visita_db.edad,
            "genero": visita_db.genero,
            "fumo_100_cigarrillos": visita_db.fumo_100_cigarrillos,
            "consumo_alcohol_ultimo_año": visita_db.consumo_alcohol_ultimo_año,
            "actividad_deportiva_moderada_x_semana": visita_db.actividad_deportiva_moderada_x_semana,
            "anhedonia": visita_db.anhedonia,
            "peso": visita_db.peso,
            "altura": visita_db.altura,
            "presion_sistolica_final": visita_db.presion_sistolica_final,
            "presion_diastolica_final": visita_db.presion_diastolica_final,
            "colesterol_total": visita_db.colesterol_total,
            "hdl": visita_db.hdl,
            "trigliceridos": visita_db.trigliceridos,
            "proteina_c": visita_db.proteina_c,
            "creatinina": visita_db.creatinina,
            "hipertension": visita_db.hipertension,
            "diabetes": visita_db.diabetes,
            "asma": visita_db.asma,
            "riñones_debiles_fallando": visita_db.riñones_debiles_fallando,
            "fam_cardio": visita_db.fam_cardio,
            "fam_diabetes": visita_db.fam_diabetes,
            "fam_asma": visita_db.fam_asma
        }

        # Decidimos etapa: si hay creatinina, es Etapa 2 (Final)
        etapa_actual = 2 if (visita_db.creatinina is not None) else 1
        
        prob_calculada, _ = predictor.ejecutar_prediccion(datos_ia, etapa=etapa_actual)
        prob_final = float(prob_calculada)

        # 4. Guardar resultados de la IA
        visita_db.probabilidad_riesgo = prob_final
        if etapa_actual == 2:
            visita_db.riesgo_final = prob_final
        else:
            visita_db.riesgo_preliminar = prob_final

        db.commit()
        db.refresh(visita_db)
        db.refresh(visita_db.paciente)
        
        print(f">>> [DB UPDATE] Visita {visita_id} actualizada. Nuevo score: {prob_final}")
        
        # Devolvemos el paciente relacionado para que el front no rompa
        return {
            "id": visita_db.paciente.id,
            "dni": visita_db.paciente.dni,
            "nombre": visita_db.paciente.nombre,
            "apellido": visita_db.paciente.apellido,
            "visita_id": visita_db.id, 
            "visitas": [visita_db] 
        }

    except Exception as e:
        db.rollback()
        print(f"Error al actualizar visita: {e}")
        raise HTTPException(status_code=500, detail=str(e))