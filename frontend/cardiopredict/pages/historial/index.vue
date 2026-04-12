<template>
  <v-container
    fluid
    class="pa-0 d-flex flex-column"
    style="
      height: calc(100vh - 64px);
      background-color: #1a1a1a;
      overflow: hidden;
    "
  >
    <v-sheet color="transparent" class="px-12 pt-12 pb-0 flex-shrink-0">
      <h2 class="white--text text-h4 mb-4 font-weight-light">
        Realizar búsqueda
      </h2>
      <p class="grey--text text--lighten-1 mb-2">
        {{ filtroDni ? "Resultados de búsqueda" : "Pacientes recientes" }}
      </p>

      <v-text-field
        v-model="filtroDni"
        solo
        background-color="#4a4444"
        dark
        class="mb-6"
        placeholder="Ingrese DNI para buscar..."
        clearable
        hide-details="auto"
        :rules="dniRules"
        @input="validarYBuscar"
      />

      <v-row
        v-if="pacientesLista.length > 0 && !buscando"
        class="grey--text text--caption px-4 mb-2"
      >
        <v-col cols="6">Apellido y nombre</v-col>
        <v-col cols="3">DNI</v-col>
        <v-col cols="3"></v-col>
      </v-row>
      <v-divider
        v-if="pacientesLista.length > 0 && !buscando"
        class="grey darken-3"
      ></v-divider>
    </v-sheet>

    <v-sheet
      color="#1a1a1a"
      class="px-12 pt-4 flex-grow-1 custom-scroll-area"
      style="overflow-y: auto"
    >
      <div v-if="buscando" class="d-flex justify-center align-center py-12">
        <v-progress-circular
          indeterminate
          color="grey darken-1"
          size="64"
          width="4"
        />
      </div>

      <div v-if="pacientesLista.length > 0 && !buscando" class="pb-16">
        <v-row
          v-for="p in pacientesLista"
          :key="p.id"
          class="white--text align-center py-3 px-4 hover-row rounded-lg mb-2"
        >
          <v-col cols="6" class="text-body-1 font-weight-light">
            {{ p.apellido }}, {{ p.nombre }}
          </v-col>
          <v-col cols="3" class="text-body-1 grey--text text--lighten-2">
            {{ p.dni }}
          </v-col>
          <v-col cols="3" class="text-right">
            <v-btn
              color="#4a4444"
              outlined
              class="white--text custom-btn"
              :to="`/historial/${p.dni}`"
            >
              VER HISTORIAL
            </v-btn>
          </v-col>
        </v-row>
      </div>

      <div
        v-else-if="
          filtroDni && filtroDni.length >= 3 && !buscando && soloNumerosValido
        "
        class="grey--text mt-12 text-center"
      >
        <v-icon color="#4a4444" size="64" class="mb-4">fas fa-search</v-icon>
        <div class="text-h6 font-weight-thin">
          No hay coincidencias para: <strong>{{ filtroDni }}</strong>
        </div>
      </div>
    </v-sheet>
  </v-container>
</template>

<script>
import { pacienteService } from "@/services/pacienteService";

export default {
  data() {
    return {
      filtroDni: "",
      pacientesLista: [],
      buscando: false,
      timeout: null,
      dniRules: [
        (v) => !v || /^\d+$/.test(v) || "El DNI debe contener solo números",
      ],
    };
  },
  computed: {
    soloNumerosValido() {
      return /^\d+$/.test(this.filtroDni);
    },
  },
  mounted() {
    this.cargarPacientesRecientes();
  },
  methods: {
    async cargarPacientesRecientes() {
      this.buscando = true;
      try {
        this.pacientesLista = await pacienteService.obtenerTodos(20);
      } catch (e) {
        console.error(e);
      } finally {
        this.buscando = false;
      }
    },
    validarYBuscar() {
      if (!this.filtroDni) {
        this.cargarPacientesRecientes();
        if (this.timeout) clearTimeout(this.timeout);
        return;
      }
      if (!this.soloNumerosValido || this.filtroDni.length < 3) {
        if (this.timeout) clearTimeout(this.timeout);
        return;
      }
      if (this.timeout) clearTimeout(this.timeout);
      this.buscando = true;
      this.timeout = setTimeout(() => {
        this.ejecutarBusqueda(this.filtroDni);
      }, 500);
    },
    async ejecutarBusqueda(dni) {
      try {
        const resultado = await pacienteService.buscarPorDni(dni);
        this.pacientesLista = Array.isArray(resultado)
          ? resultado
          : [resultado];
      } catch (error) {
        console.error("Error en búsqueda:", error);
        this.pacientesLista = [];
      } finally {
        this.buscando = false;
      }
    },
  },
};
</script>

<style scoped>
/* Sombras para dar un toque de profundidad a las filas */
.hover-row {
  background-color: #222; /* Un gris apenas más claro para que resalten las cards */
  border: 1px solid transparent;
  transition: all 0.2s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.hover-row:hover {
  background-color: #2a2a2a;
  border-color: #444;
  transform: translateY(-2px);
  cursor: pointer;
}

.custom-btn {
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

/* Barra de scroll personalizada acorde al fondo #1a1a1a */
.custom-scroll-area::-webkit-scrollbar {
  width: 8px;
}
.custom-scroll-area::-webkit-scrollbar-track {
  background: #1a1a1a;
}
.custom-scroll-area::-webkit-scrollbar-thumb {
  background: #333;
  border-radius: 4px;
}
.custom-scroll-area::-webkit-scrollbar-thumb:hover {
  background: #444;
}
</style>
