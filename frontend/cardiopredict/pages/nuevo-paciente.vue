<template>
  <FormularioPaciente
    :modoEdicion="false"
    @atras="$router.push('/')"
    @finalizar="guardarNuevoPaciente"
  />
</template>

<script>
import FormularioPaciente from "@/components/FormularioPaciente.vue";

export default {
  components: {
    FormularioPaciente,
  },
  methods: {
    guardarNuevoPaciente() {
      // Aquí irá tu lógica de POST a la API más adelante
      alert("Paciente creado con éxito");
      this.$router.push("/");
    },
  },
};
</script>
