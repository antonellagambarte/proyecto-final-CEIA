import shap
import os
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier

# --- SECCIÓN 1: Rutas y Configuración ---
BASE_DIR = os.path.dirname(__file__)
PATH_E1 = os.path.join(BASE_DIR, 'modelos', 'random_forest_optuna_under_etapa1.joblib')
PATH_E2 = os.path.join(BASE_DIR, 'modelos', 'random_forest_optuna_under_etapa2.joblib')
PATH_ENCODERS = os.path.join(BASE_DIR, "encoders", "encoders_categoricos.joblib")
PATH_SCALER = os.path.join(BASE_DIR, "scalers", "scaler_cardio.joblib")

VARS_LOGARITMICAS = [
    'trigliceridos', 'colesterol_total', 'bmi', 'presion_sistolica_final', 
    'presion_diastolica_final', 'proteina_c', 'hemoglobina', 'hdl', 'acido_urico', 'potasio'
]

UMBRAL_ETAPA1 = 0.4
UMBRAL_ETAPA2 = 0.4

MAPA_NOMBRES = {
    'edad': 'Edad', 'genero': 'Género', 'fumo_100_cigarrillos': 'Tabaquismo',
    'actividad_deportiva_moderada_x_semana': 'Actividad Física',
    'consumo_alcohol_ultimo_año': 'Consumo Alcohol', 'anhedonia': 'Anhedonia',
    'bmi': 'IMC', 'presion_sistolica_final': 'P. Sistólica',
    'presion_diastolica_final': 'P. Diastólica', 'fam_cardio_2.0': 'Ant. Familiar Cardio',
    'fam_diabetes_2.0': 'Ant. Familiar Diabetes', 'fam_asma_9.0': 'Ant. Familiar Asma',
    'riñones_debiles_fallando_2.0': 'Problemas Renales', 'hipertension_2': 'Hipertensión',
    'diabetes_2.0': 'Diabetes', 'colesterol_total': 'Colesterol', 'hdl': 'HDL',
    'trigliceridos': 'Triglicéridos', 'proteina_c': 'Prot. C Reactiva'
}

# --- SECCIÓN 2: Carga de modelos ---
modelo1, modelo2 = None, None
explainer1, explainer2 = None, None
encoders_dict, scaler = {}, None

try:
    modelo1 = joblib.load(PATH_E1)
    modelo2 = joblib.load(PATH_E2)
    encoders_dict = joblib.load(PATH_ENCODERS)
    scaler = joblib.load(PATH_SCALER)
    # Inicialización de Explainers
    if modelo1: explainer1 = shap.TreeExplainer(modelo1) 
    if modelo2: explainer2 = shap.TreeExplainer(modelo2)
    print("Pipeline de IA y SHAP listos.")
except Exception as e:
    print(f"Error crítico cargando archivos: {e}")

# --- SECCIÓN 4: Función de Predicción ---
def ejecutar_prediccion(datos_dict, etapa=1):
    print(f"\n>>> [DEBUG] Datos recibidos del Frontend (Etapa {etapa}):")
    print(datos_dict)
    
    df = pd.DataFrame([datos_dict])
    modelo = modelo1 if etapa == 1 else modelo2
    explainer = explainer1 if etapa == 1 else explainer2
    
    if modelo is None: 
        return 0.0, []

    # --- PREPROCESAMIENTO ---
    if 'peso' in df.columns and 'altura' in df.columns:
        try:
            p = float(df['peso'].iloc[0])
            a = float(df['altura'].iloc[0])
            df['bmi'] = p / (a ** 2) if a > 0 else 0
        except:
            df['bmi'] = 0

    for col in VARS_LOGARITMICAS:
        if col in df.columns:
            df[col] = np.log1p(pd.to_numeric(df[col], errors='coerce').fillna(0))

    # Encoding
    for col_nombre, encoder_obj in encoders_dict.items():
        if col_nombre in df.columns:
            try:
                nuevas_cols = encoder_obj.get_feature_names_out([col_nombre])
                df[nuevas_cols] = encoder_obj.transform(df[[col_nombre]])
            except: 
                pass

    # Alineación de columnas
    columnas_entrenamiento = getattr(modelo, "feature_names_in_", [])
    df_ia = df.reindex(columns=columnas_entrenamiento).fillna(0)
    
    # Scaler
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
            print(f">>> [DEBUG] Error en Scaler: {e}")

    # --- 1. CÁLCULO DE PROBABILIDAD (Aislado) ---
    try:
        # Asegurar que df_ia esté limpio antes de predecir
        df_ia = df_ia.reindex(columns=columnas_entrenamiento).fillna(0)
        
        # Forzamos la obtención de la probabilidad y la convertimos a float estándar
        prob_raw = modelo.predict_proba(df_ia)[0][1]
        probabilidad = round(float(prob_raw), 4)
        
        print(f"\n>>> [DEBUG] PROBABILIDAD EXITOSA: {probabilidad}")
    except Exception as e:
        print(f">>> [DEBUG] Error fatal en predict_proba: {e}")
        return 0.0, []

    # --- 2. CÁLCULO DE SHAP (Con su propio try/except) ---
    influencias = []
    try:
        if explainer:
            raw_shap_values = explainer.shap_values(df_ia)
            
            # Ajuste para Random Forest: si devuelve lista [clase0, clase1], usamos clase1
            if isinstance(raw_shap_values, list):
                shap_values_final = raw_shap_values[1][0]
            else:
                # Si es un array 3D (algunas versiones de SHAP), tomamos la base
                if len(raw_shap_values.shape) == 3:
                    shap_values_final = raw_shap_values[0, :, 1]
                else:
                    shap_values_final = raw_shap_values[0]

            for col, val in zip(columnas_entrenamiento, shap_values_final):
                if abs(val) > 0.001: 
                    influencias.append({
                        "feature": MAPA_NOMBRES.get(col, col),
                        "valor": round(float(val), 4)
                    })
            
            influencias = sorted(influencias, key=lambda x: abs(x["valor"]), reverse=True)
        else:
            print(">>> [DEBUG] Explainer no disponible.")
            
    except Exception as e:
        # Si SHAP falla, imprimimos el error pero NO reseteamos la probabilidad
        print(f">>> [DEBUG] SHAP falló (influencias vacías), pero se mantiene prob: {e}")

    # Retornamos la probabilidad calculada en el paso 1
    return probabilidad, influencias