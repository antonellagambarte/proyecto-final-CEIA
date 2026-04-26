<template>
  <v-card flat color="transparent" class="white--text">
    <div v-for="(item, index) in influencias" :key="index" class="mb-4">
      <div class="d-flex justify-space-between align-end mb-1">
        <span class="text-caption font-weight-bold grey--text text--lighten-1">
          {{ item.feature.toUpperCase() }}
        </span>
        <span
          :class="item.valor > 0 ? 'red--text' : 'cyan--text'"
          class="text-caption font-weight-black"
        >
          {{ item.valor > 0 ? "+" : "" }}{{ (item.valor * 100).toFixed(2) }}%
        </span>
      </div>

      <v-progress-linear
        :value="calcularPorcentaje(item.valor)"
        :color="item.valor > 0 ? 'red darken-2' : 'cyan darken-2'"
        height="12"
        rounded
        background-opacity="0.1"
      >
        <template v-slot:default="{ value }"> </template>
      </v-progress-linear>
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
