from fastapi import FastAPI
import models  # Importamos el archivo de modelos
from database import engine, Base # Importamos la conexión

# Esta línea crea las tablas en el archivo .db si no existen todavía
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API de CardioPredict conectada a la base de datos"}