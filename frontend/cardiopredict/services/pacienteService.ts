import { Paciente } from "~/types/paciente";

const API_URL = "http://localhost:8000";

export const pacienteService = {
  async guardar(payload: any): Promise<Paciente> {
    try {
      const isUpdate = !!payload.id;
      const url = isUpdate
        ? `${API_URL}/pacientes/${payload.id}`
        : `${API_URL}/pacientes/`;

      const response = await fetch(url, {
        method: isUpdate ? "PUT" : "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error("Error al procesar la solicitud");
      return await response.json();
    } catch (error) {
      console.error("Error en el service:", error);
      throw error;
    }
  },

  async buscarPorDni(dni: string): Promise<Paciente[]> {
    try {
      const response = await fetch(`${API_URL}/pacientes/buscar/${dni}`);
      if (!response.ok) return [];
      return await response.json();
    } catch (error) {
      console.error("Error buscando por DNI:", error);
      return [];
    }
  },

  async predecirAlVuelo(payload: any) {
    try {
      const response = await fetch(`${API_URL}/pacientes/predecir`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!response.ok) throw new Error("Error en la predicción");
      return await response.json();
    } catch (error) {
      console.error("Error al predecir:", error);
      throw error;
    }
  },

  async obtenerTodos(top: number | null = null): Promise<Paciente[]> {
    try {
      const url = top
        ? `${API_URL}/pacientes/?top=${top}`
        : `${API_URL}/pacientes/`;
      const response = await fetch(url);
      if (!response.ok) throw new Error("Error al obtener pacientes");
      return await response.json();
    } catch (error) {
      console.error("Error obteniendo pacientes:", error);
      return [];
    }
  },
};
