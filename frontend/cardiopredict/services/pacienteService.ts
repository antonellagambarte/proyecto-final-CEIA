import { Paciente } from "~/types/paciente";

const API_URL = "http://localhost:8000";

export const pacienteService = {
  async guardar(payload) {
    try {
      if (payload.id) {
        // Si tiene ID, se usa PUT para actualizar
        const response = await fetch(
          `http://localhost:8000/pacientes/${payload.id}`,
          {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
          }
        );
        return await response.json();
      } else {
        // Si NO tiene ID, se usa POST para crear uno nuevo
        const response = await fetch("http://localhost:8000/pacientes/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        return await response.json();
      }
    } catch (error) {
      console.error("Error en el service:", error);
      throw error;
    }
  },

  async buscarPorDni(dni: string): Promise<Paciente[]> {
    const response = await fetch(`${API_URL}/pacientes/buscar/${dni}`);

    if (!response.ok) return [];

    return await response.json();
  },
};
