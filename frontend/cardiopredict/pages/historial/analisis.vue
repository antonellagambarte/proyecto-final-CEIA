<template>
  <v-container fluid class="main-container pa-0">

    <!-- MODAL DE AYUDA -->
    <v-dialog v-model="modalAyuda" max-width="620" scrollable>
      <v-card color="#252525" dark>
        <v-card-title class="d-flex align-center py-5 px-6" style="border-bottom: 1px solid #3a3a3a">
          <v-icon color="cyan lighten-2" class="mr-3">fas fa-question-circle</v-icon>
          <span class="white--text text-h6 font-weight-light">¿Cómo leer este gráfico?</span>
          <v-spacer></v-spacer>
          <v-btn icon small @click="modalAyuda = false">
            <v-icon small color="grey lighten-1">fas fa-times</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="px-6 pt-6 pb-2" style="max-height: 70vh; overflow-y: auto">

          <p class="grey--text text--lighten-1 body-2 mb-6">
            Este gráfico muestra cuáles características del paciente
            <strong class="white--text">aumentaron</strong> o
            <strong class="white--text">redujeron</strong> su probabilidad de riesgo cardiovascular,
            y en qué medida influyó cada una en el resultado.
          </p>

          <!-- PROBABILIDAD DE REFERENCIA -->
          <div class="mb-6">
            <div class="d-flex align-center mb-3">
              <div style="width: 3px; height: 22px; background: rgba(0,229,255,0.8); border-radius: 2px" class="mr-3"></div>
              <span class="white--text font-weight-medium">La probabilidad de referencia</span>
            </div>
            <p class="grey--text text--lighten-1 body-2 mb-0" style="padding-left: 18px">
              Es la probabilidad promedio de riesgo cardiovascular calculada sobre la
              población de referencia utilizada para entrenar el modelo. Representa el punto
              de partida antes de considerar los datos individuales de este paciente.
            </p>
          </div>

          <v-divider class="grey darken-3 mb-6"></v-divider>

          <!-- EJEMPLOS DE BARRAS -->
          <div class="mb-2">
            <span class="white--text font-weight-medium d-block mb-5">Las barras</span>

            <!-- Barra positiva (roja) -->
            <div class="d-flex align-center mb-5">
              <div style="
                width: 130px; min-width: 130px; height: 30px;
                background: linear-gradient(90deg, #ef5350, #ff7043);
                clip-path: polygon(0 0, calc(100% - 12px) 0, 100% 50%, calc(100% - 12px) 100%, 0 100%);
                border-radius: 4px;
              " class="mr-5"></div>
              <div>
                <div class="red--text text--lighten-1 caption font-weight-bold mb-1">INCREMENTA LA PROBABILIDAD DE RIESGO →</div>
                <p class="grey--text text--lighten-1 body-2 mb-0">
                  Esta característica aumentó la probabilidad de riesgo cardiovascular
                  por encima de la referencia. Cuanto más larga la barra, mayor es su peso en el resultado.
                </p>
              </div>
            </div>

            <!-- Barra negativa (cyan) -->
            <div class="d-flex align-center mb-2">
              <div style="
                width: 130px; min-width: 130px; height: 30px;
                background: linear-gradient(90deg, #00bcd4, #26c6da);
                clip-path: polygon(12px 0, 100% 0, 100% 100%, 12px 100%, 0 50%);
                border-radius: 4px;
              " class="mr-5"></div>
              <div>
                <div class="cyan--text text--lighten-1 caption font-weight-bold mb-1">← REDUCE LA PROBABILIDAD DE RIESGO</div>
                <p class="grey--text text--lighten-1 body-2 mb-0">
                  Esta característica redujo la probabilidad de riesgo cardiovascular
                  por debajo de la referencia. Cuanto más larga la barra, mayor es su peso en el resultado.
                </p>
              </div>
            </div>
          </div>

          <v-divider class="grey darken-3 my-5"></v-divider>

          <p class="grey--text caption mb-4">
            El número dentro de cada barra indica cuánto desplazó ese factor la probabilidad
            de riesgo, en la misma escala que el resultado final (0 a 1). Por ejemplo, si la
            probabilidad de referencia es 0.44 y una barra muestra 0.05, ese factor llevó la
            probabilidad a 0.49. La suma de todas las barras sobre la probabilidad de
            referencia da como resultado la probabilidad final estimada para este paciente.
          </p>

        </v-card-text>

        <v-card-actions class="px-6 py-4" style="border-top: 1px solid #3a3a3a">
          <v-spacer></v-spacer>
          <v-btn text color="cyan lighten-2" class="px-6" @click="modalAyuda = false">ENTENDIDO</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-sheet color="transparent" class="px-12 pt-12 pb-6">
      <v-btn text small dark @click="$router.go(-1)" class="mb-4 grey--text">
        <v-icon left small>fas fa-arrow-left</v-icon>
        Volver al informe
      </v-btn>

      <div class="d-flex align-center justify-space-between">
        <div class="d-flex align-center">
          <h2 class="white--text text-h4 font-weight-thin">
            Análisis comparativo de riesgo
          </h2>

          <v-chip class="ml-4" color="rgb(67, 160, 71)" small label dark>
            <span class="black--text">
              {{ paciente.apellido }}, {{ paciente.nombre }}
            </span>
          </v-chip>
        </div>

        <v-btn
          outlined
          color="cyan lighten-2"
          @click="modalAyuda = true"
        >
          <v-icon left small>fas fa-question-circle</v-icon>
          ¿Cómo leer el gráfico?
        </v-btn>
      </div>
    </v-sheet>

    <!-- TARJETAS ARRIBA -->
    <v-row class="px-12 pb-6">
      <!-- PRELIMINAR -->
      <v-col cols="12" md="6">
        <v-card
          dark
          color="#252525"
          class="pa-6 h-100"
          rounded="lg"
          style="border-left: 5px solid #ffb300"
        >
          <div class="grey--text text-caption mb-1">PREDICCIÓN PRELIMINAR</div>

          <div
            :class="[
              'text-h4 font-weight-black',
              resultado.preliminar.probabilidad >= 0.4
                ? 'amber--text'
                : 'green--text text--lighten-1',
            ]"
          >
            {{
              resultado.preliminar.probabilidad >= 0.4
                ? "RIESGO ALTO"
                : "RIESGO BAJO"
            }}
          </div>

          <div class="text-caption grey--text mt-1">
            Basado en historia clínica
          </div>
        </v-card>
      </v-col>

      <!-- FINAL -->
      <v-col cols="12" md="6">
        <v-card
          v-if="resultado.final.probabilidad"
          dark
          color="#252525"
          class="pa-6 h-100"
          rounded="lg"
          style="border-left: 5px solid #7e57c2"
        >
          <div class="grey--text text-caption mb-1">PREDICCIÓN FINAL</div>

          <div
            :class="[
              'text-h4 font-weight-black',
              resultado.final.probabilidad >= 0.4
                ? 'purple--text text--lighten-2'
                : 'green--text text--lighten-1',
            ]"
          >
            {{
              resultado.final.probabilidad >= 0.4
                ? "RIESGO ALTO"
                : "RIESGO BAJO"
            }}
          </div>

          <div class="text-caption grey--text">
            Basado en historia clínica y resultados de laboratorio
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- GRÁFICO ABAJO -->
    <v-row class="px-4 pb-12">
      <v-col cols="12">
        <v-card dark color="#252525" class="pa-8" rounded="lg">
          <v-tabs v-model="tab" color="cyan" grow class="mb-6">
            <v-tab> Factores que influyen en el resultado preliminar </v-tab>

            <v-tab v-if="resultado.final.influencias.length">
              Factores que influyen en el resultado final
            </v-tab>
          </v-tabs>

          <v-tabs-items v-model="tab" class="transparent">
            <v-tab-item
              v-for="(res, index) in [resultado.preliminar, resultado.final]"
              :key="index"
            >
              <div class="grafico-scroll-container">
                <GraficoInfluencia
                  :influencias="res.influencias"
                  :base-value="res.baseValue"
                  :prediccion="res.probabilidad"
                />
              </div>
            </v-tab-item>
          </v-tabs-items>

        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { pacienteService } from "@/services/pacienteService";

export default {
  data() {
    return {
      visitaId: this.$route.query.visitaId,
      dni: this.$route.query.dni,
      tab: 0,
      cargando: true,
      modalAyuda: false,
      paciente: {},
      resultado: {
        preliminar: { probabilidad: 0, influencias: [] },
        final: { probabilidad: 0, influencias: [] },
      },
    };
  },

  computed: {
    diferenciaRiesgo() {
      if (
        this.resultado.final.probabilidad &&
        this.resultado.preliminar.probabilidad
      ) {
        return (
          this.resultado.final.probabilidad -
          this.resultado.preliminar.probabilidad
        );
      }
      return 0;
    },
  },

  async mounted() {
    await this.obtenerAnalisis();
  },

  methods: {
    async obtenerAnalisis() {
      this.cargando = true;
      try {
        const visita = await pacienteService.obtenerVisitaPorId(this.visitaId);

        if (!visita) return;

        this.paciente = {
          nombre: visita.paciente.nombre,
          apellido: visita.paciente.apellido,
        };

        if (visita.riesgo_preliminar == null) {
          const payload = {
            edad: visita.edad,
            genero: visita.genero,
            fumo_100_cigarrillos: visita.fumo_100_cigarrillos,
            consumo_alcohol_ultimo_año: visita.consumo_alcohol_ultimo_año,
            actividad_deportiva_moderada_x_semana:
              visita.actividad_deportiva_moderada_x_semana,
            anhedonia: visita.anhedonia,
            peso: visita.peso,
            altura: visita.altura,
            presion_sistolica_final: visita.presion_sistolica_final,
            presion_diastolica_final: visita.presion_diastolica_final,
            hipertension: visita.hipertension,
            diabetes: visita.diabetes,
            asma: visita.asma,
            riñones_debiles_fallando: visita.riñones_debiles_fallando,
            fam_cardio: visita.fam_cardio,
            fam_diabetes: visita.fam_diabetes,
            fam_asma: visita.fam_asma,
          };

          console.log("VISITA; ", visita);

          const res = await pacienteService.predecirAlVuelo(payload, true);
          this.resultado.preliminar = {
            probabilidad: res.probabilidad,
            influencias: res.influencias || [],
            baseValue: visita.base_value_preliminar || 0.44,
          };
        } else {
          this.resultado.preliminar = {
            probabilidad: visita.riesgo_preliminar || 0,
            influencias: visita.influencias_preliminares || [],
            baseValue: visita.base_value_preliminar || 0.44,
          };
        }
        console.log("VISITA; ", visita);
        this.resultado.final = {
          probabilidad: visita.riesgo_final || 0,
          influencias: visita.influencias_finales || [],
          baseValue: visita.base_value_final || 0.44,
        };

        if (this.resultado.final.probabilidad > 0) {
          this.tab = 1;
        }
      } catch (e) {
        console.error("Error cargando análisis comparativo:", e);
      } finally {
        this.cargando = false;
      }
    },
  },
};
</script>

<style scoped>
.grafico-scroll-container {
  overflow-y: auto;
  padding-right: 15px;
  padding-bottom: 28px;
  mask-image: linear-gradient(to bottom, black 92%, transparent 100%);
}

.grafico-scroll-container::-webkit-scrollbar {
  width: 6px;
}

.grafico-scroll-container::-webkit-scrollbar-track {
  background: #1a1a1a;
}

.grafico-scroll-container::-webkit-scrollbar-thumb {
  background: #444;
  border-radius: 10px;
}

.grafico-scroll-container::-webkit-scrollbar-thumb:hover {
  background: #00e5ff;
}

.v-tabs-items {
  background-color: transparent !important;
}

.main-container {
  height: 100vh;
  overflow-y: auto;
  overflow-x: hidden;
  background-color: #1a1a1a;
  padding-left: 256px;

  /* scroll suave */
  scroll-behavior: smooth;

  /* Firefox */
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.08) transparent;

  mask-image: linear-gradient(
    to bottom,
    transparent 0%,
    black 2%,
    black 98%,
    transparent 100%
  );
}

/* Chrome / Edge / Opera */
.main-container::-webkit-scrollbar {
  width: 6px;
}

.main-container::-webkit-scrollbar-track {
  background: transparent;
}

.main-container::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  transition: all 0.3s ease;
}

.main-container::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.16);
}

/* opcional: esconder flechas */
.main-container::-webkit-scrollbar-button {
  display: none;
}
</style>
