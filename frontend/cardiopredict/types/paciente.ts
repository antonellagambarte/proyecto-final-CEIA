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
