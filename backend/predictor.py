import shap
import os
import pandas as pd
import numpy as np
import joblib

# --- SECCIÓN 1: Rutas y Configuración ---
BASE_DIR = os.path.dirname(__file__)
PATH_E1 = os.path.join(BASE_DIR, 'modelos', 'rf_under_optuna_model_etapa1.joblib')
PATH_E2 = os.path.join(BASE_DIR, 'modelos', 'rf_under_optuna_model_etapa2.joblib')
PATH_ENCODERS = os.path.join(BASE_DIR, "encoders", "encoders_categoricos.joblib")
PATH_SCALER = os.path.join(BASE_DIR, "scalers", "scaler_cardio.joblib")

VARS_LOGARITMICAS = [
    'trigliceridos', 'colesterol_total', 'bmi', 'presion_sistolica_final', 
    'presion_diastolica_final', 'proteina_c', 'hemoglobina', 'hdl', 'acido_urico', 'potasio'
]

UMBRAL_ETAPA1 = 0.4
UMBRAL_ETAPA2 = 0.4

MAPA_NOMBRES = {
    'edad': 'Edad', 'genero': 'Género', 'fumo_100_cigarrillos': 'Ant. de tabaquismo',
    'actividad_deportiva_moderada_x_semana': 'Actividad Física',
    'consumo_alcohol_ultimo_año': 'Consumo Alcohol', 'anhedonia': 'Anhedonia',
    'bmi': 'IMC', 'presion_sistolica_final': 'P. Sistólica',
    'presion_diastolica_final': 'P. Diastólica', 
    'fam_cardio': 'ant. familiares ECV',
    'fam_diabetes': 'ant. familiares de diabetes',
    'fam_asma': 'ant. familiares de asma',
    'riñones_debiles_fallando': 'problemas renales',
    'hipertension': 'hipertensión',
    'diabetes': 'diabetes',
    'asma': 'asma',
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
    df = pd.DataFrame([datos_dict])
    modelo = modelo1 if etapa == 1 else modelo2
    explainer = explainer1 if etapa == 1 else explainer2
    
    if modelo is None: 
        return 0.0, [], 0.0

    # Guardamos copia para identificar el estado clínico original (1, 2 o 9)
    datos_originales = datos_dict.copy()

    if 'peso' in df.columns and 'altura' in df.columns:
        try:
            p = float(df['peso'].iloc[0])
            a = float(df['altura'].iloc[0])
            df['bmi'] = p / (a ** 2) if a > 0 else 0
        except: df['bmi'] = 0

    for col in VARS_LOGARITMICAS:
        if col in df.columns:
            df[col] = np.log1p(pd.to_numeric(df[col], errors='coerce').fillna(0))

    for col_nombre, encoder_obj in encoders_dict.items():
        if col_nombre in df.columns:
            try:
                nuevas_cols = encoder_obj.get_feature_names_out([col_nombre])
                df[nuevas_cols] = encoder_obj.transform(df[[col_nombre]])
            except: pass

    columnas_entrenamiento = getattr(modelo, "feature_names_in_", [])
    df_ia = df.reindex(columns=columnas_entrenamiento).fillna(0)

    if scaler:
        try:
            VARS_SCALER = scaler.feature_names_in_
            df_para_escalar = df.reindex(columns=VARS_SCALER).fillna(0)
            valores_escalados = scaler.transform(df_para_escalar)
            df_escalado_final = pd.DataFrame(valores_escalados, columns=VARS_SCALER)
            for col in df_ia.columns:
                if col in VARS_SCALER: df_ia[col] = df_escalado_final[col].values
        except Exception as e: print(f"Error Scaler: {e}")

    try:
        prob_raw = modelo.predict_proba(df_ia)[0][1]
        probabilidad = round(float(prob_raw), 4)
    except: return 0.0, [], 0.0

    influencias = []
    base_value = 0.0
    try:
        if explainer:
            raw_shap_values = explainer.shap_values(df_ia)
            
            # Ajuste para Random Forest (Clase 1)
            if isinstance(raw_shap_values, list):
                shap_values_final = raw_shap_values[1][0]
                base_value = float(explainer.expected_value[1])
            else:
                if len(raw_shap_values.shape) == 3:
                    shap_values_final = raw_shap_values[0, :, 1]
                    base_value = float(explainer.expected_value[1])
                else:
                    shap_values_final = raw_shap_values[0]
                    base_value = float(explainer.expected_value)

            acumulado = {}
            for col, val in zip(columnas_entrenamiento, shap_values_final):
                # Detectar nombre base sin sufijos de dummy
                nombre_base = col
                for sufijo in ['_2.0', '_9.0', '_2', '_9', '_3.0']:
                    if col.endswith(sufijo):
                        nombre_base = col.replace(sufijo, '')
                        break
                
                # Acumulamos (Suma de dummies = Aproximación del impacto de la variable)
                acumulado[nombre_base] = acumulado.get(nombre_base, 0) + float(val)

            total_abs = sum(abs(v) for v in acumulado.values())
            for var_key, total_val in acumulado.items():
                if abs(total_val) > 0.0001:
                    nombre_display = MAPA_NOMBRES.get(var_key, var_key)
                    val_original = datos_originales.get(var_key)

                    # Lógica de construcción de etiqueta clínica
                    if var_key in ['fam_cardio', 'fam_diabetes', 'fam_asma', 'riñones_debiles_fallando', 'hipertension', 'diabetes', 'asma', 'fumo_100_cigarrillos']:
                        if val_original == 1 or val_original == 1.0:
                            nombre_display = f"Tiene {nombre_display}"
                        elif val_original == 2 or val_original == 2.0:
                            nombre_display = f"No tiene {nombre_display}"
                        elif val_original == 9 or val_original == 9.0:
                            nombre_display = f"Desconoce {nombre_display}"

                    porcentaje = (abs(total_val) / total_abs) * 100 if total_abs > 0 else 0
                    influencias.append({
                        "feature": nombre_display,
                        "valor": round(total_val, 4),
                        "porcentaje": round(porcentaje, 2)
                    })
            
            influencias = sorted(influencias, key=lambda x: abs(x["valor"]), reverse=True)
    except Exception as e: print(f"SHAP Error: {e}")
    print("BASE:", base_value)
    print("SHAP SUM:", np.sum(shap_values_final))
    print("TOTAL:", base_value + np.sum(shap_values_final))
    print("PROB:", probabilidad)
    return probabilidad, influencias, round(base_value, 4)