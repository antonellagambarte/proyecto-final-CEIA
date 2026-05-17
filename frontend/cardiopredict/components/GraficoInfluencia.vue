<template>
  <v-card flat color="transparent" class="white--text pa-2">
    <div class="waterfall-layout">
      <div class="labels-column">
        <div
          v-for="(item, i) in waterfallData"
          :key="'label-' + i"
          class="feature-label"
        >
          {{ item.feature }}
        </div>
      </div>

      <div class="waterfall-scroll">
        <div class="waterfall-chart">
          <div
            v-for="(item, i) in waterfallData"
            :key="'bar-' + i"
            class="waterfall-row"
          >
            <div class="waterfall-container">
              <div
                class="base-line"
                :style="{ left: baseLineLeft + '%' }"
              ></div>

              <div
                class="waterfall-bar"
                :class="item.valor > 0 ? 'positive-bar' : 'negative-bar'"
                :style="{
                  left: item.left + '%',
                  width: item.width + '%',
                }"
              >
                <span class="bar-text">
                  {{ formatValor(item.valor) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </v-card>
</template>

<script>
export default {
  props: {
    influencias: {
      type: Array,
      default: () => [],
    },

    baseValue: {
      type: Number,
      default: 0.44,
    },
  },

  computed: {
    waterfallData() {
      const ESCALA = 85;

      const ordenadas = [...this.influencias].sort(
        (a, b) => Math.abs(a.valor) - Math.abs(b.valor)
      );

      let acumulado = this.baseValue;

      const completas = ordenadas.map((item) => {
        const inicio = acumulado;
        const fin = acumulado + item.valor;

        acumulado = fin;

        return {
          ...item,
          inicio,
          fin,
          magnitud: Math.abs(item.valor),
        };
      });

      const top10 = [...completas]
        .sort((a, b) => b.magnitud - a.magnitud)
        .slice(0, 10);

      const todosLosValores = [
        this.baseValue,
        ...top10.map((x) => x.inicio),
        ...top10.map((x) => x.fin),
      ];

      const min = Math.min(...todosLosValores);
      const max = Math.max(...todosLosValores);
      const rango = Math.max(max - min, 0.05);

      return top10.map((item) => {
        const startPercent = ((item.inicio - min) / rango) * ESCALA;
        const endPercent = ((item.fin - min) / rango) * ESCALA;

        return {
          ...item,
          left: Math.min(startPercent, endPercent),
          width: Math.abs(endPercent - startPercent),
        };
      });
    },

    baseLineLeft() {
      const valores = [
        this.baseValue,
        ...this.waterfallData.map((x) => x.inicio),
        ...this.waterfallData.map((x) => x.fin),
      ];

      const min = Math.min(...valores);
      const max = Math.max(...valores);
      const rango = Math.max(max - min, 0.05);

      return ((this.baseValue - min) / rango) * 85;
    },
  },

  methods: {
    formatValor(valor) {
      return Math.abs(valor).toFixed(4);
    },
  },
};
</script>

<style scoped>
.waterfall-layout {
  display: flex;
  width: 100%;
}

.labels-column {
  width: 145px;
  min-width: 145px;
  flex-shrink: 0;
  z-index: 2;
  background: #252525;
}

.feature-label {
  height: 56px;
  display: flex;
  align-items: center;
  color: white;
  font-size: 0.95rem;
  padding-right: 12px;
}

.waterfall-scroll {
  flex: 1;
  overflow-x: auto;
  overflow-y: hidden;
  padding-bottom: 8px;
}

.waterfall-chart {
  min-width: 760px;
  width: calc(100% - 32px);
  margin-left: 16px;
  margin-right: 16px;
}

.waterfall-row {
  height: 56px;
  display: flex;
  align-items: center;
}

.waterfall-container {
  position: relative;
  width: 100%;
  height: 36px;
}

.base-line {
  position: absolute;
  top: 0;
  width: 2px;
  height: 100%;
  background: rgba(255, 255, 255, 0.18);
  transform: translateX(-50%);
}

.waterfall-bar {
  box-sizing: border-box;
  position: absolute;
  top: 5px;
  height: 26px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  transition: all 0.4s ease;
  overflow: hidden;
}

.negative-bar {
  background: linear-gradient(90deg, #00bcd4, #26c6da);
  justify-content: flex-end;
  padding-right: 12px;
  clip-path: polygon(12px 0, 100% 0, 100% 100%, 12px 100%, 0 50%);
}

.positive-bar {
  background: linear-gradient(90deg, #ef5350, #ff7043);
  justify-content: flex-start;
  padding-left: 12px;
  clip-path: polygon(
    0 0,
    calc(100% - 12px) 0,
    100% 50%,
    calc(100% - 12px) 100%,
    0 100%
  );
}

.bar-text {
  color: white;
  font-size: 0.78rem;
  font-weight: 600;
  z-index: 2;
  white-space: nowrap;
}
</style>
