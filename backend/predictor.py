import os
import pandas as pd
import numpy as np
import joblib
from catboost import CatBoostClassifier

# --- SECCIÓN 1: Rutas y Configuración ---
BASE_DIR = os.path.dirname(__file__)
PATH_E1 = os.path.join(BASE_DIR, "modelos", "modelo_catboost_etapa1.joblib")
PATH_E2 = os.path.join(BASE_DIR, "modelos", "modelo_catboost_etapa2.joblib")
PATH_ENCODERS = os.path.join(BASE_DIR, "encoders", "encoders_categoricos.joblib")
PATH_SCALER = os.path.join(BASE_DIR, "scalers", "scaler_cardio.joblib")

# Lista de variables que requieren log1p según entrenamiento
VARS_LOGARITMICAS = [
    'trigliceridos', 'colesterol_total', 'bmi', 'presion_sistolica_final', 
    'presion_diastolica_final', 'glicohemoglobina', 'proteina_c',
    'ancho_distribucion_globulos', 'hemoglobina', 'hdl', 'acido_urico',
    'enzima_tgp', 'enzima_tgo', 'sodio', 'potasio'
]

# --- SECCIÓN 2: Carga de modelos ---
modelo1 = CatBoostClassifier()
modelo2 = CatBoostClassifier()
encoders_dict = {}
scaler = None

try:
    modelo1 = joblib.load(PATH_E1)
    modelo2 = joblib.load(PATH_E2)
    encoders_dict = joblib.load(PATH_ENCODERS)
    scaler = joblib.load(PATH_SCALER)
    print("Pipeline de IA cargado: Modelos, Encoders y Scaler listos.")
except Exception as e:
    print(f"Error crítico cargando archivos: {e}")

# --- SECCIÓN 3: Columnas del Modelo ---
COLUMNAS_MODELO_1 = [
    'edad', 'genero', 'fumo_100_cigarrillos', 'actividad_deportiva_moderada_x_semana',
    'consumo_alcohol_ultimo_año_1.0', 'consumo_alcohol_ultimo_año_2.0', 'consumo_alcohol_ultimo_año_3.0',
    'consumo_alcohol_ultimo_año_4.0', 'consumo_alcohol_ultimo_año_5.0', 'consumo_alcohol_ultimo_año_6.0',
    'consumo_alcohol_ultimo_año_7.0', 'consumo_alcohol_ultimo_año_8.0', 'consumo_alcohol_ultimo_año_9.0',
    'consumo_alcohol_ultimo_año_10.0', 'consumo_alcohol_ultimo_año_20.0', 'consumo_alcohol_ultimo_año_99.0',
    'anhedonia_1.0', 'anhedonia_2.0', 'anhedonia_3.0', 'anhedonia_9.0',
    'bmi', 'presion_sistolica_final', 'presion_diastolica_final', 'fam_cardio_2.0', 
    'fam_diabetes_2.0', 'fam_asma_9.0', 'riñones_debiles_fallando_2.0',
    'hipertension_2', 'diabetes_2.0'
]

COLUMNAS_MODELO_2 = COLUMNAS_MODELO_1 + [
    'colesterol_total', 'hdl', 'trigliceridos', 'proteina_c', 
    'hemoglobina', 'creatinina', 'acido_urico', 'potasio'
]

# --- SECCIÓN 4: Función de Predicción ---
def ejecutar_prediccion(datos_dict, etapa=1):
    df = pd.DataFrame([datos_dict])
    
    if 'peso' in df.columns and 'altura' in df.columns:
        try:
            df['bmi'] = df['peso'] / (df['altura'] ** 2)
        except ZeroDivisionError:
            df['bmi'] = 0

    for col in VARS_LOGARITMICAS:
        if col in df.columns:
            df[col] = np.log1p(pd.to_numeric(df[col], errors='coerce').fillna(0))

    for col_nombre, encoder_obj in encoders_dict.items():
        if col_nombre in df.columns:
            try:
                nuevas_cols = encoder_obj.get_feature_names_out([col_nombre])
                df[nuevas_cols] = encoder_obj.transform(df[[col_nombre]])
                df.drop(columns=[col_nombre], inplace=True)
            except Exception as e:
                print(f"Aviso OHE: {col_nombre}: {e}")

    columnas_finales = COLUMNAS_MODELO_1 if etapa == 1 else COLUMNAS_MODELO_2
    df_ia = df.reindex(columns=columnas_finales).fillna(0)

    if scaler:
        try:
            VARS_SCALER = scaler.feature_names_in_
            df_para_escalar = df.reindex(columns=VARS_SCALER).fillna(0)
            
            valores_escalados = scaler.transform(df_para_escalar)
            df_escalado_final = pd.DataFrame(valores_escalados, columns=VARS_SCALER)
            
            for col in df_ia.columns:
                if col in VARS_SCALER:
                    df_ia[col] = df_escalado_final[col].values
        except Exception as e:
            print(f"Error en escalado: {e}")

    try:
        modelo = modelo1 if etapa == 1 else modelo2
        probabilidad = modelo.predict_proba(df_ia)[0][1]
    except Exception as e:
        print(f"Error en predict_proba: {e}")
        return 0.0
        
    return round(float(probabilidad), 4)