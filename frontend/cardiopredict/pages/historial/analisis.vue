<template>
  <v-container
    fluid
    class="pa-0"
    style="min-height: 100vh; background-color: #1a1a1a"
  >
    <v-sheet color="transparent" class="px-12 pt-12 pb-6">
      <v-btn text small dark @click="$router.go(-1)" class="mb-4 grey--text">
        <v-icon left small>fas fa-arrow-left</v-icon> Volver al informe
      </v-btn>

      <div class="d-flex align-center">
        <h2 class="white--text text-h4 font-weight-thin">
          Análisis Comparativo de Riesgo
        </h2>
        <v-chip class="ml-4" color="cyan" small label dark>
          {{ paciente.apellido }}, {{ paciente.nombre }}
        </v-chip>
      </div>
    </v-sheet>

    <v-row class="px-12 pb-12">
      <v-col cols="12" md="4">
        <v-card
          dark
          color="#252525"
          class="pa-6 mb-4"
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
          <div class="text-caption grey--text mt-1">Basado en hábitos</div>
        </v-card>

        <v-card
          v-if="resultado.final.probabilidad"
          dark
          color="#252525"
          class="pa-6"
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
          <v-divider class="my-3 grey darken-3"></v-divider>
          <div class="text-caption grey--text">Análisis con biomarcadores</div>
        </v-card>
      </v-col>

      <v-col cols="12" md="8">
        <v-card dark color="#252525" class="pa-8" rounded="lg">
          <v-tabs v-model="tab" color="cyan" grow class="mb-6">
            <v-tab>Influencia en predicción preliminar</v-tab>
            <v-tab v-if="resultado.final.influencias.length">
              Influencia en predicción final
            </v-tab>
          </v-tabs>

          <v-tabs-items v-model="tab" class="transparent">
            <v-tab-item
              v-for="(res, index) in [resultado.preliminar, resultado.final]"
              :key="index"
            >
              <div class="grafico-scroll-container">
                <GraficoInfluencia :influencias="res.influencias" />
              </div>
            </v-tab-item>
          </v-tabs-items>

          <v-divider class="my-4 grey darken-3"></v-divider>

          <div class="d-flex justify-space-between pt-2 px-2">
            <div class="cyan--text text--lighten-2 caption">
              <v-icon x-small color="cyan lighten-2" class="mr-1">
                fas fa-arrow-down
              </v-icon>
              Disminuye predicción del modelo
            </div>

            <div class="red--text text--lighten-2 caption">
              Aumenta predicción del modelo
              <v-icon x-small color="red lighten-2" class="ml-1">
                fas fa-arrow-up
              </v-icon>
            </div>
          </div>
          <div class="grey--text text--lighten-1 caption mt-4">
            El modelo estima un nivel de riesgo inicial basado en su
            entrenamiento y lo ajusta según los factores individuales del
            paciente. Cada variable puede aumentar o disminuir la probabilidad
            final de riesgo. /Los porcentajes muestran cuánto contribuye cada
            factor al resultado final del modelo en este paciente, en relación
            con los demás factores./Los porcentajes representan la importancia
            relativa de cada factor dentro de la explicación del modelo para
            este paciente.
          </div>
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
          const res = await pacienteService.predecirAlVuelo(payload, true);
          this.resultado.preliminar = {
            probabilidad: res.probabilidad,
            influencias: res.influencias || [],
          };
        } else {
          this.resultado.preliminar = {
            probabilidad: visita.riesgo_preliminar || 0,
            influencias: visita.influencias_preliminares || [],
          };
        }

        this.resultado.final = {
          probabilidad: visita.riesgo_final || 0,
          influencias: visita.influencias_finales || [],
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
  max-height: 480px;
  overflow-y: auto;
  padding-right: 15px;
  mask-image: linear-gradient(to bottom, black 95%, transparent 100%);
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
</style>
