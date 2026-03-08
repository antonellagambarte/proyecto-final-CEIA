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
      alert("Paciente creado con éxito");
      this.$router.push("/");
    },
  },
};
</script>
