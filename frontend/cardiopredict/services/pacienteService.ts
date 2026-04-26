import { Paciente } from "~/types/paciente";

const API_URL = "http://localhost:8000";

export const pacienteService = {
  // Ahora "guardar" siempre hace POST porque cada consulta es una nueva Visita
  // En tu pacienteService.ts

  async guardar(
    payload: any,
    visitaId: number | null = null
  ): Promise<Paciente> {
    try {
      // Si viene un visitaId, usamos PUT para actualizar la visita existente
      const url = visitaId
        ? `${API_URL}/visitas/${visitaId}`
        : `${API_URL}/pacientes/`;

      const method = visitaId ? "PUT" : "POST";

      const response = await fetch(url, {
        method: method,
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
      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error buscando por DNI:", error);
      return [];
    }
  },

  async obtenerVisitas(pacienteId: number) {
    try {
      const response = await fetch(
        `${API_URL}/pacientes/${pacienteId}/visitas`
      );
      if (!response.ok) throw new Error("Error al obtener visitas");
      return await response.json();
    } catch (error) {
      console.error("Error en obtenerVisitas:", error);
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

  actualizarVisita(visitaId, datos) {
    return axios.put(`/visitas/${visitaId}`, datos);
  },
};
