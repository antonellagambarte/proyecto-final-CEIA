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

# MAPEO ACTUALIZADO: Agregadas variantes 2.0, 3.0 y 9.0 para consolidar
MAPA_NOMBRES = {
    'edad': 'Edad', 'genero': 'Género', 'fumo_100_cigarrillos': 'Tabaquismo',
    'actividad_deportiva_moderada_x_semana': 'Actividad Física',
    'consumo_alcohol_ultimo_año': 'Consumo Alcohol', 'anhedonia': 'Anhedonia',
    'bmi': 'IMC', 'presion_sistolica_final': 'P. Sistólica',
    'presion_diastolica_final': 'P. Diastólica', 
    'fam_cardio_2.0': 'Ant. Familiar Cardio', 'fam_cardio_9.0': 'Ant. Familiar Cardio',
    'fam_diabetes_2.0': 'Ant. Familiar Diabetes', 'fam_diabetes_9.0': 'Ant. Familiar Diabetes',
    'fam_asma_2.0': 'Ant. Familiar Asma', 'fam_asma_9.0': 'Ant. Familiar Asma',
    'riñones_debiles_fallando_2.0': 'Problemas Renales', 'riñones_debiles_fallando_9.0': 'Problemas Renales',
    'hipertension_2': 'Hipertensión', 'hipertension_9': 'Hipertensión',
    'diabetes_2.0': 'Diabetes', 'diabetes_3.0': 'Diabetes', 'diabetes_9.0': 'Diabetes',
    'asma_2.0': 'Asma', 'asma_9.0': 'Asma',
    'colesterol_total': 'Colesterol', 'hdl': 'HDL',
    'trigliceridos': 'Triglicéridos', 'proteina_c': 'Prot. C Reactiva',
    'hemoglobina': 'Hemoglobina', 'creatinina': 'Creatinina',
    'acido_urico': 'Ácido Úrico', 'potasio': 'Potasio'
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

    for col_nombre, encoder_obj in encoders_dict.items():
        if col_nombre in df.columns:
            try:
                nuevas_cols = encoder_obj.get_feature_names_out([col_nombre])
                df[nuevas_cols] = encoder_obj.transform(df[[col_nombre]])
            except: 
                pass

    columnas_entrenamiento = getattr(modelo, "feature_names_in_", [])
    df_ia = df.reindex(columns=columnas_entrenamiento).fillna(0)
    
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

    try:
        df_ia = df_ia.reindex(columns=columnas_entrenamiento).fillna(0)
        prob_raw = modelo.predict_proba(df_ia)[0][1]
        probabilidad = round(float(prob_raw), 4)
    except Exception as e:
        print(f">>> [DEBUG] Error fatal en predict_proba: {e}")
        return 0.0, []

    influencias = []
    try:
        if explainer:
            raw_shap_values = explainer.shap_values(df_ia)
            if isinstance(raw_shap_values, list):
                shap_values_final = raw_shap_values[1][0]
            else:
                shap_values_final = raw_shap_values[0, :, 1] if len(raw_shap_values.shape) == 3 else raw_shap_values[0]

            acumulado = {}
            for col, val in zip(columnas_entrenamiento, shap_values_final):
                nombre = MAPA_NOMBRES.get(col, col)
                acumulado[nombre] = acumulado.get(nombre, 0) + float(val)
                
            total_abs = sum(abs(v) for v in acumulado.values())

            for nombre, total_val in acumulado.items():
                if abs(total_val) > 0.001: 
                    porcentaje = (abs(total_val) / total_abs) * 100 if total_abs > 0 else 0
                    influencias.append({
                        "feature": nombre,
                        "valor": round(total_val, 4),
                        "porcentaje": round(porcentaje, 2)
                    })
            # ---------------------------------------
            
            influencias = sorted(influencias, key=lambda x: abs(x["valor"]), reverse=True)
        else:
            print(">>> [DEBUG] Explainer no disponible.")
    except Exception as e:
        print(f">>> [DEBUG] SHAP falló: {e}")

    return probabilidad, influencias