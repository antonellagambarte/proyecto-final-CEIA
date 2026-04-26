export interface Visita {
  id: number;
  paciente_id: number;
  fecha_visita: string;

  // Datos clínicos de la consulta
  edad: number | null;
  genero: number | null;
  fumo_100_cigarrillos: number | null;
  consumo_alcohol_ultimo_año: number | null;
  actividad_deportiva_moderada_x_semana: number | null;
  anhedonia: number | null;
  peso: number | null;
  altura: number | null;
  bmi: number | null;
  presion_sistolica_final: number | null;
  presion_diastolica_final: number | null;

  // Antecedentes y laboratorio
  fam_cardio: number | null;
  fam_diabetes: number | null;
  fam_asma: number | null;
  riñones_debiles_fallando: number | null;
  hipertension: number | null;
  diabetes: number | null;
  asma: number | null;

  colesterol_total: number | null;
  hdl: number | null;
  trigliceridos: number | null;
  proteina_c: number | null;
  hemoglobina: number | null;
  creatinina: number | null;
  acido_urico: number | null;
  potasio: number | null;

  // Resultados de la IA
  riesgo_preliminar?: number | null;
  riesgo_final?: number | null;
  probabilidad_riesgo?: number | null;
}

export interface Paciente {
  id: number;
  dni: string;
  nombre: string;
  apellido: string;
  fecha_creacion?: string;
  // Un paciente ahora tiene una lista de visitas
  visitas: Visita[];
}

// Mantenemos esta para el tipado del formulario de entrada
export interface FormularioPaciente extends Partial<Visita> {
  dni: string;
  nombre: string;
  apellido: string;
}
