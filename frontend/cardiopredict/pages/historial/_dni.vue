<template>
  <div>
    <v-container
      v-if="!verDetalleForm"
      fluid
      class="pa-12"
      style="background-color: #1a1a1a; min-height: 100vh"
    >
      <div
        class="d-flex align-center mb-6 cursor-pointer"
        @click="$router.back()"
      >
        <v-icon small color="grey">fas fa-arrow-left</v-icon>
        <span class="grey--text caption ml-2">Volver a búsqueda</span>
      </div>

      <h2 class="white--text text-h4 mb-8 font-weight-light">
        Historial: {{ paciente.apellido }}, {{ paciente.nombre }}
      </h2>

      <v-row class="grey--text text--caption mb-2 px-4">
        <v-col cols="3">Fecha</v-col>
        <v-col cols="3">Estado estudios</v-col>
        <v-col cols="6"></v-col>
      </v-row>
      <v-divider class="grey darken-3 mb-4"></v-divider>

      <v-row
        v-for="(h, i) in historialFicticio"
        :key="i"
        class="white--text align-center py-4 px-4 border-bottom"
      >
        <v-col cols="3">{{ h.fecha }}</v-col>
        <v-col cols="3">
          <v-chip
            small
            :color="h.estado === 'Completo' ? 'success' : 'warning'"
            outlined
          >
            {{ h.estado }}
          </v-chip>
        </v-col>
        <v-col cols="6" class="text-right">
          <v-btn outlined color="#a39a9a" class="mr-4 custom-btn" small
            >VER PREDICCIONES</v-btn
          >
          <v-btn
            color="#635b5b"
            class="white--text custom-btn"
            small
            @click="irADetalle(h)"
            >VER DATOS</v-btn
          >
        </v-col>
      </v-row>
    </v-container>

    <FormularioPaciente
      v-else
      :datosIniciales="datosEstudioSeleccionado"
      :modoEdicion="true"
      @atras="verDetalleForm = false"
    />
  </div>
</template>

<script>
// Importamos el componente (asegúrate de haberlo creado en components/FormularioPaciente.vue)
import FormularioPaciente from "@/components/FormularioPaciente.vue";

export default {
  components: {
    FormularioPaciente,
  },
  asyncData({ params }) {
    const dni = params.dni;
    return { dni };
  },
  data() {
    return {
      verDetalleForm: false, // Switch para cambiar de vista
      datosEstudioSeleccionado: null, // Aquí guardaremos los datos que verá el formulario
      paciente: { nombre: "Juan", apellido: "Pérez", dni: "30152486" },
      historialFicticio: [
        { id: 1, fecha: "05/03/2025", estado: "Pendiente" },
        { id: 2, fecha: "22/07/2025", estado: "Completo" },
      ],
    };
  },
  methods: {
    irADetalle(estudio) {
      // 1. Cargamos datos ficticios para ese estudio (esto vendrá de tu API después)
      this.datosEstudioSeleccionado = {
        apellido: this.paciente.apellido,
        nombre: this.paciente.nombre,
        dni: this.paciente.dni,
        genero: "Masculino",
        edad: estudio.id === 2 ? "52" : "51", // Ejemplo de datos variando
        // ... aquí irían todos los campos (diabetes, presión, lab, etc)
      };

      // 2. Cambiamos la vista
      this.verDetalleForm = true;
    },
  },
};
</script>

<style scoped>
.border-bottom {
  border-bottom: 1px solid #333;
}
.custom-btn {
  font-size: 0.7rem;
}
</style>
