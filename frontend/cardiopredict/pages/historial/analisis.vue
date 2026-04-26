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
          style="border-top: 4px solid #ffb300"
        >
          <div class="grey--text text-caption mb-1">
            RIESGO PRELIMINAR (HÁBITOS)
          </div>
          <div class="text-h3 font-weight-black amber--text">
            {{ (resultado.preliminar.probabilidad * 100).toFixed(1) }}%
          </div>
          <div class="text-caption grey--text mt-2">
            Basado en antecedentes y estilo de vida
          </div>
        </v-card>

        <v-card
          v-if="paciente.riesgo_final"
          dark
          color="#252525"
          class="pa-6"
          rounded="lg"
          style="border-top: 4px solid #7e57c2"
        >
          <div class="grey--text text-caption mb-1">
            RIESGO FINAL (LABORATORIO)
          </div>
          <div class="text-h3 font-weight-black purple--text text--lighten-2">
            {{ (resultado.final.probabilidad * 100).toFixed(1) }}%
          </div>
          <div class="text-caption grey--text mt-2">
            Incluye biomarcadores y química sanguínea
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" md="8">
        <v-card dark color="#252525" class="pa-8" rounded="lg">
          <div
            v-if="cargando"
            class="d-flex flex-column justify-center align-center py-12"
          >
            <v-progress-circular indeterminate color="cyan" size="50" />
            <span class="mt-4 grey--text">Generando explicaciones SHAP...</span>
          </div>

          <div v-else>
            <v-tabs
              v-model="tab"
              background-color="transparent"
              color="cyan"
              grow
              class="mb-6"
            >
              <v-tab>Análisis Hábitos</v-tab>
              <v-tab v-if="paciente.riesgo_final">Análisis Laboratorio</v-tab>
            </v-tabs>

            <v-tabs-items v-model="tab" class="transparent">
              <v-tab-item>
                <div class="scroll-container">
                  <GraficoInfluencia
                    :influencias="resultado.preliminar.influencias"
                  />
                </div>
              </v-tab-item>

              <v-tab-item v-if="paciente.riesgo_final">
                <div class="scroll-container">
                  <GraficoInfluencia
                    :influencias="resultado.final.influencias"
                  />
                </div>
              </v-tab-item>
            </v-tabs-items>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { pacienteService } from "@/services/pacienteService";
import GraficoInfluencia from "@/components/GraficoInfluencia.vue";

export default {
  components: { GraficoInfluencia },
  data() {
    return {
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
  async mounted() {
    await this.obtenerAnalisis();
  },
  methods: {
    async obtenerAnalisis() {
      this.cargando = true;
      try {
        // 1. Cargar datos del paciente
        const lista = await pacienteService.buscarPorDni(this.dni);
        this.paciente = lista.length > 0 ? lista[0] : {};

        // 2. FORZAR ANÁLISIS PRELIMINAR (Para obtener las barras de Etapa 1)
        // Limpiamos los campos de lab para que el modelo use solo etapa 1
        const datosSoloHabitos = { ...this.paciente };
        const camposLab = [
          "creatinina",
          "hdl",
          "trigliceridos",
          "colesterol_total",
          "proteina_c",
          "hemoglobina",
          "acido_urico",
          "potasio",
        ];
        camposLab.forEach((campo) => (datosSoloHabitos[campo] = null));

        const resPre = await pacienteService.predecirAlVuelo(datosSoloHabitos);
        this.resultado.preliminar = {
          probabilidad: this.paciente.riesgo_preliminar || resPre.probabilidad,
          influencias: resPre.influencias || [],
        };

        // 3. ANÁLISIS FINAL (Si tiene datos o ya tiene el riesgo final guardado)
        if (this.paciente.riesgo_final || this.paciente.creatinina) {
          const resFin = await pacienteService.predecirAlVuelo(this.paciente);
          this.resultado.final = {
            probabilidad: this.paciente.riesgo_final || resFin.probabilidad,
            influencias: resFin.influencias || [],
          };
          this.tab = 1; // Por defecto mostramos la pestaña de laboratorio
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
.scroll-container {
  max-height: 550px;
  overflow-y: auto;
  padding-right: 15px;
}
/* Estilo del scrollbar */
.scroll-container::-webkit-scrollbar {
  width: 6px;
}
.scroll-container::-webkit-scrollbar-track {
  background: #252525;
}
.scroll-container::-webkit-scrollbar-thumb {
  background: #444;
  border-radius: 10px;
}
.scroll-container::-webkit-scrollbar-thumb:hover {
  background: #00e5ff;
}

/* Hacer que el fondo de las pestañas sea transparente para que no choque con el fondo oscuro */
.v-tabs-items {
  background-color: transparent !important;
}
</style>
