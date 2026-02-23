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
        class="mb-10"
        max-width="600"
        placeholder="Ej: 3015..."
        clearable
      ></v-text-field>

      <div v-if="pacientesFiltrados.length > 0">
        <v-row class="grey--text text--caption px-4">
          <v-col cols="6">Apellido y nombre</v-col>
          <v-col cols="3">DNI</v-col>
          <v-col cols="3"></v-col>
        </v-row>
        <v-divider class="grey darken-3 mb-2"></v-divider>

        <v-row
          v-for="p in pacientesFiltrados"
          :key="p.dni"
          class="white--text align-center py-2 px-4 hover-row"
        >
          <v-col cols="6" class="text-body-1"
            >{{ p.apellido }}, {{ p.nombre }}</v-col
          >
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
      <div v-else-if="filtroDni" class="grey--text mt-4">
        No se encontraron pacientes con ese DNI.
      </div>
    </v-sheet>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      filtroDni: "",
      // Datos ficticios que luego vendrán de tu API
      pacientes: [
        { nombre: "Juan", apellido: "Pérez", dni: "30152486" },
        { nombre: "Josefa", apellido: "Giménez", dni: "30158797" },
        { nombre: "Carlos", apellido: "Sánchez", dni: "22456789" },
      ],
    };
  },
  computed: {
    pacientesFiltrados() {
      if (!this.filtroDni) return [];
      return this.pacientes.filter((p) => p.dni.includes(this.filtroDni));
    },
  },
};
</script>

<style scoped>
.hover-row:hover {
  background-color: rgba(255, 255, 255, 0.05);
}
.custom-btn {
  font-size: 0.75rem;
  font-weight: bold;
}
</style>
