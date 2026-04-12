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
      // this.$router.push("/");
    },
  },
};
</script>
