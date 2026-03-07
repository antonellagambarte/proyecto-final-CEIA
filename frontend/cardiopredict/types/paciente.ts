export interface FormularioPaciente {
  dni: string;
  nombre: string;
  apellido: string;
  sexo: string;
  fuma: string;
  presion_sistolica: number | null;
  colesterol_total: number | null;
  creatinina: number | null;
}

export interface Paciente {
  id?: number;
  apellido: string;
  nombre: string;
  genero: "Masculino" | "Femenino";
  dni: string;
  edad: number | null;

  // Estilo de vida
  diabetico: number | null;
  renales: number | null;
  alcohol: number | null;
  ejercicio: number | null;
  fumador: string | null;
  anhedonia: number | null;

  fam_cardio: string | null;
  fam_diabetes: string | null;
  fam_asma: string | null;

  // Datos físicos y laboratorio
  altura: number | null;
  peso: number | null;
  presion_sis: number | null;
  presion_dis: number | null;
  hdl: number | null;
  trigliceridos: number | null;
  colesterol: number | null;
  creatinina: number | null;
  pcr: number | null;
  hemoglobina: number | null;
  acido_urico: number | null;
  potasio: number | null;
}
