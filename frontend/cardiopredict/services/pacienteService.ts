import { Paciente } from "~/types/paciente";

const API_URL = "http://localhost:8000";

export const pacienteService = {
  async guardar(datos: Paciente): Promise<Paciente> {
    const esEdicion = !!datos.id;
    const url = esEdicion
      ? `${API_URL}/pacientes/${datos.id}`
      : `${API_URL}/pacientes`;
    const method = esEdicion ? "PUT" : "POST";

    const response = await fetch(url, {
      method: method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos),
    });

    if (!response.ok) {
      throw new Error("Error al conectar con el servidor de salud");
    }

    return await response.json();
  },

  async buscarPorDni(dni: string): Promise<Paciente[]> {
    // Ahora devuelve un Array
    const response = await fetch(`${API_URL}/pacientes/buscar/${dni}`);

    if (!response.ok) return [];

    return await response.json();
  },
};
