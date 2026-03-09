<template>
  <v-container
    fluid
    class="pa-0 d-flex flex-column"
    style="height: calc(100vh - 100px); background-color: #1a1a1a"
  >
    <v-sheet color="transparent" class="pa-12 flex-grow-1">
      <h2 class="white--text text-h4 mb-4 font-weight-light">
        Realizar búsqueda
      </h2>
      <p class="grey--text text--lighten-1 mb-2">Ingrese el DNI del paciente</p>

      <v-text-field
        v-model="filtroDni"
        solo
        background-color="#4a4444"
        dark
        class="mb-6"
        placeholder="Ej: 3015..."
        clearable
        :rules="dniRules"
        @input="validarYBuscar"
      />

      <div v-if="buscando" class="d-flex justify-center align-center py-12">
        <v-progress-circular
          indeterminate
          color="grey lighten-1"
          size="80"
          width="5"
        />
      </div>

      <div v-if="pacientesLista.length > 0 && !buscando">
        <v-row class="grey--text text--caption px-4">
          <v-col cols="6">Apellido y nombre</v-col>
          <v-col cols="3">DNI</v-col>
          <v-col cols="3"></v-col>
        </v-row>
        <v-divider class="grey darken-3 mb-2"></v-divider>

        <v-row
          v-for="p in pacientesLista"
          :key="p.id"
          class="white--text align-center py-2 px-4 hover-row"
        >
          <v-col cols="6" class="text-body-1">
            {{ p.apellido }}, {{ p.nombre }}
          </v-col>
          <v-col cols="3" class="text-body-1">{{ p.dni }}</v-col>
          <v-col cols="3" class="text-right">
            <v-btn
              color="#635b5b"
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
        class="grey--text mt-4"
      >
        No se encontraron pacientes con ese DNI.
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
  methods: {
    validarYBuscar() {
      if (!this.filtroDni) {
        this.filtroDni = "";
        this.pacientesLista = [];
        this.buscando = false;
        if (this.timeout) clearTimeout(this.timeout);
        return;
      }

      if (!this.soloNumerosValido) {
        this.pacientesLista = [];
        this.buscando = false;
        if (this.timeout) clearTimeout(this.timeout);
        return;
      }

      if (this.filtroDni.length < 3) {
        this.pacientesLista = [];
        this.buscando = false;
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
.hover-row:hover {
  background-color: rgba(255, 255, 255, 0.05);
  cursor: pointer;
}
.custom-btn {
  font-size: 0.75rem;
  font-weight: bold;
}
</style>
