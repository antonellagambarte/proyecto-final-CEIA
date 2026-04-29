<template>
  <v-card flat color="transparent" class="white--text">
    <div v-for="(item, i) in influencias" :key="i" class="mb-4">
      <div class="d-flex justify-space-between align-center mb-1">
        <div class="white--text text-body-2">
          {{ item.feature }}
        </div>

        <div class="d-flex align-center">
          <v-icon
            x-small
            class="mr-1"
            :color="item.valor > 0 ? 'red lighten-2' : 'cyan lighten-2'"
          >
            {{ item.valor > 0 ? "fas fa-arrow-up" : "fas fa-arrow-down" }}
          </v-icon>

          <span
            :class="
              item.valor > 0
                ? 'red--text text--lighten-2'
                : 'cyan--text text--lighten-2'
            "
            class="text-caption"
          >
            {{ item.porcentaje }}%
          </span>
        </div>
      </div>

      <v-progress-linear
        :value="item.porcentaje"
        height="8"
        :color="item.valor > 0 ? 'red' : 'cyan'"
        rounded
      />
    </div>
  </v-card>
</template>

<script>
export default {
  props: {
    // Aquí pasas el array 'influencias' que viene del backend
    influencias: {
      type: Array,
      default: () => [],
    },
  },
  // En el script de GraficoInfluencia.vue, cambia el método:
  methods: {
    calcularPorcentaje(valor) {
      // SHAP para modelos binarios suele ser pequeño (ej: 0.1, 0.2).
      // Si lo dejamos solo con Math.abs(valor) * 100, las barras quedan muy cortas.
      // Usamos un factor de escala para que la variable de mayor peso ocupe el ~90% de la barra
      const valoresAbs = this.influencias.map((i) => Math.abs(i.valor));
      const maxVal = Math.max(...valoresAbs, 0.1); // Evitamos división por cero

      return (Math.abs(valor) / maxVal) * 100;
    },
  },
};
</script>

<style scoped>
.v-progress-linear {
  border-radius: 4px;
  transition: all 0.5s ease;
}
</style>
