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
              ></div>

              <span
                class="bar-text"
                :class="{
                  'inside-text': item.width >= 5,
                  'outside-text': item.width < 5,
                  'positive-text': item.valor > 0,
                  'negative-text': item.valor < 0,
                }"
                :style="{
                  left:
                    item.width >= 5
                      ? item.left + item.width / 2 + '%'
                      : item.valor > 0
                      ? item.left + item.width + '%'
                      : item.left + '%',
                }"
              >
                {{ formatValor(item.valor) }}
              </span>
            </div>
          </div>

          <!-- EJE -->
          <div class="axis-row">
            <div class="axis-line"></div>

            <div
              v-for="(tick, i) in axisTicks"
              :key="'tick-' + i"
              class="axis-marker"
              :style="{ left: tick.left + '%' }"
            >
              <div class="axis-tick"></div>
              <div class="axis-label">
                {{ tick.valor.toFixed(3) }}
              </div>
            </div>

            <div class="axis-base-marker" :style="{ left: baseLineLeft + '%' }">
              <div class="axis-tick base-tick"></div>
              <div class="axis-label base-label">
                Base: {{ baseValue.toFixed(3) }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </v-card>
</template>

<script>
const ESCALA = 85;

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
    prediccion: {
      type: Number,
      default: null,
    },
  },

  computed: {
    waterfallData() {
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

      const { min, rango } = this.getAxisInfo(top10);

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

    axisInfo() {
      return this.getAxisInfo(this.waterfallData);
    },

    baseLineLeft() {
      const { min, rango } = this.axisInfo;
      return ((this.baseValue - min) / rango) * ESCALA;
    },

    axisTicks() {
      const { min, rango } = this.axisInfo;

      return [0, 0.25, 0.5, 0.75, 1].map((p) => ({
        valor: min + rango * p,
        left: p * ESCALA,
      }));
    },
  },

  methods: {
    formatValor(valor) {
      return Math.abs(valor).toFixed(4);
    },

    getAxisInfo(items) {
      console.log("props: ", this.$props);

      const valores = [
        this.baseValue,
        this.prediccion,
        ...items.map((x) => x.inicio),
        ...items.map((x) => x.fin),
      ].filter((v) => v !== null && v !== undefined);

      const min = Math.min(...valores);
      const max = Math.max(...valores);
      const rango = Math.max(max - min, 0.05);

      return { min, max, rango };
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
  width: 170px;
  min-width: 170px;
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
  min-width: 730px;
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
  overflow: visible;
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
  position: absolute;
  top: 50%;
  font-size: 0.78rem;
  font-weight: 600;
  white-space: nowrap;
  z-index: 5;
}

.inside-text {
  color: white;
  transform: translate(-50%, -50%);
}

.outside-text {
  color: white;
}

.positive-text.outside-text {
  transform: translate(8px, -50%);
}

.negative-text.outside-text {
  transform: translate(calc(-100% - 8px), -50%);
}

/* ===== EJE ===== */

.axis-row {
  position: relative;
  height: 40px;
  margin-top: 8px;
}

.axis-line {
  position: absolute;
  top: 8px;
  left: 0;
  width: 85%;
  height: 1px;
  background: rgba(255, 255, 255, 0.22);
}

.axis-marker,
.axis-base-marker {
  position: absolute;
  top: 0;
  transform: translateX(-50%);
  font-size: 0.72rem;
  white-space: nowrap;
}

.axis-tick {
  width: 1px;
  height: 9px;
  background: rgba(255, 255, 255, 0.35);
  margin: 0 auto 4px auto;
}

.axis-label {
  color: rgba(255, 255, 255, 0.55);
}

.base-tick {
  width: 2px;
  height: 12px;
  background: rgba(0, 229, 255, 0.75);
}

.base-label {
  color: rgba(0, 229, 255, 0.9);
  font-weight: 600;
  position: relative;
  top: 12px;
}
</style>
