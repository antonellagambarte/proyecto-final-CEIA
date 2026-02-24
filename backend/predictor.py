import os
import pandas as pd
from catboost import CatBoostClassifier

# --- SECCIÓN 1: Rutas a la carpeta /modelos ---
BASE_DIR = os.path.dirname(__file__)
# Apuntamos a la subcarpeta 'modelos'
PATH_E1 = os.path.join(BASE_DIR, "modelos", "modelo_catboost_etapa1.joblib")
PATH_E2 = os.path.join(BASE_DIR, "modelos", "modelo_catboost_etapa2.joblib")

# --- SECCIÓN 2: Carga de modelos ---
modelo1 = CatBoostClassifier()
modelo2 = CatBoostClassifier()

try:
    # CatBoost puede cargar archivos .joblib o .cbm directamente
    modelo1.load_model(PATH_E1)
    modelo2.load_model(PATH_E2)
    print("✅ Modelos CatBoost cargados correctamente desde /modelos")
except Exception as e:
    print(f"⚠️ Error cargando modelos: {e}")

# --- SECCIÓN 3: Predicción ---
def ejecutar_prediccion(datos_dict, etapa=1):
    # Convertimos a DataFrame (CatBoost lo prefiere)
    df = pd.DataFrame([datos_dict])
    
    # IMPORTANTE: Aquí podrías necesitar filtrar las columnas 
    # para que coincidan exactamente con las que usaste al entrenar.
    
    if etapa == 1:
        # predict_proba devuelve [[prob_clase_0, prob_clase_1]]
        probabilidad = modelo1.predict_proba(df)[0][1]
    else:
        probabilidad = modelo2.predict_proba(df)[0][1]
        
    return round(float(probabilidad), 4)