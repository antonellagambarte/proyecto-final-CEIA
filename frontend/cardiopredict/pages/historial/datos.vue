<template>
  <div>
    <v-container
      v-if="!mostrandoEdicion"
      fluid
      class="pa-0 d-flex flex-column"
      style="height: calc(100vh - 64px); background-color: #1a1a1a"
    >
      <v-sheet color="transparent" class="px-12 pt-12 pb-6 flex-shrink-0">
        <div class="d-flex justify-space-between align-start">
          <div>
            <v-btn
              text
              small
              dark
              :to="`/historial/${pacienteDni}`"
              class="mb-4 px-0 grey--text text--lighten-1"
              style="text-transform: none; letter-spacing: normal"
            >
              <v-icon small color="grey lighten-1">fas fa-arrow-left</v-icon>
              Volver a historiales
            </v-btn>

            <div class="d-flex align-center mb-2">
              <h2 class="white--text text-h4 font-weight-light">
                Informe de Datos:
                {{
                  cargando
                    ? "Cargando..."
                    : `${paciente.apellido}, ${paciente.nombre}`
                }}
              </h2>
            </div>
            <p class="grey--text text--lighten-1 mb-0">
              DNI: {{ pacienteDni || "-" }} | Registro:
              {{ formatearFecha(paciente.fecha_creacion) }}
            </p>
          </div>

          <v-btn
            v-if="!cargando && !estaCompleto"
            color="amber darken-2"
            outlined
            dark
            rounded
            class="mt-10"
            style="text-transform: none"
            @click="irAEditar"
          >
            <v-icon left small>fas fa-pencil</v-icon>
            Completar datos faltantes
          </v-btn>
        </div>
      </v-sheet>

      <v-sheet
        color="#121212"
        class="px-12 pt-6 flex-grow-1 custom-scroll-area"
        style="overflow-y: auto; border-top: 1px solid #2d2d2d"
      >
        <div v-if="cargando" class="d-flex justify-center align-center py-12">
          <v-progress-circular
            indeterminate
            color="grey darken-1"
            size="64"
            width="4"
          />
        </div>

        <div v-else class="pb-16 white--text">
          <section class="mb-10">
            <h3
              class="text-h5 font-weight-thin grey--text text--lighten-2 mb-5"
            >
              1. Datos Personales
            </h3>
            <v-row>
              <v-col cols="12" md="4">
                <div class="label-info">APELLIDO Y NOMBRE</div>
                <div class="text-body-1">
                  {{ paciente.apellido }}, {{ paciente.nombre }}
                </div>
              </v-col>
              <v-col cols="6" md="2">
                <div class="label-info">GÉNERO</div>
                <div class="text-body-1">
                  {{ traducirGenero(paciente.genero) }}
                </div>
              </v-col>
              <v-col cols="6" md="2">
                <div class="label-info">EDAD</div>
                <div class="text-body-1">{{ paciente.edad || "-" }} años</div>
              </v-col>
            </v-row>
          </section>

          <v-divider class="grey darken-4 mb-10"></v-divider>

          <section class="mb-10">
            <h3
              class="text-h5 font-weight-thin grey--text text--lighten-2 mb-5"
            >
              2. Antecedentes Médicos
            </h3>
            <v-row>
              <v-col cols="6" md="3">
                <div class="label-info">DIABETES</div>
                <div class="text-body-1">
                  {{ traducirOpcion(paciente.diabetes, "diabetes") }}
                </div>
              </v-col>
              <v-col cols="6" md="3">
                <div class="label-info">HIPERTENSIÓN</div>
                <div class="text-body-1">
                  {{ traducirOpcion(paciente.hipertension) }}
                </div>
              </v-col>
              <v-col cols="6" md="3">
                <div class="label-info">PROBLEMAS RENALES</div>
                <div class="text-body-1">
                  {{ traducirOpcion(paciente.riñones_debiles_fallando) }}
                </div>
              </v-col>
              <v-col cols="6" md="3">
                <div class="label-info">HISTORIAL DE TABAQUISMO</div>
                <div class="text-body-1">
                  {{ traducirBinario(paciente.fumo_100_cigarrillos) }}
                </div>
              </v-col>
            </v-row>
          </section>

          <v-divider class="grey darken-4 mb-10"></v-divider>

          <section class="mb-10">
            <h3
              class="text-h5 font-weight-thin grey--text text--lighten-2 mb-5"
            >
              3. Estilo de Vida y Salud Mental
            </h3>
            <v-row>
              <v-col cols="6" md="4">
                <div class="label-info">CONSUMO DE ALCOHOL</div>
                <div class="text-body-1">
                  {{ traducirAlcohol(paciente.consumo_alcohol_ultimo_año) }}
                </div>
              </v-col>
              <v-col cols="6" md="4">
                <div class="label-info">ACTIVIDAD FÍSICA MODERADA</div>
                <div class="text-body-1">
                  {{ paciente.actividad_deportiva_moderada_x_semana || 0 }} días
                  por semana
                </div>
              </v-col>
              <v-col cols="12" md="4">
                <div class="label-info">PRESENCIA DE ANHEDONIA</div>
                <div class="text-body-1">
                  {{ traducirAnhedonia(paciente.anhedonia) }}
                </div>
              </v-col>
            </v-row>
          </section>

          <v-divider class="grey darken-4 mb-10"></v-divider>

          <section class="mb-10">
            <h3
              class="text-h5 font-weight-thin grey--text text--lighten-2 mb-5"
            >
              4. Antecedentes Familiares
            </h3>
            <v-row>
              <v-col cols="6" md="3">
                <div class="label-info">CARDIOVASCULAR</div>
                <div class="text-body-1">
                  {{ traducirOpcion(paciente.fam_cardio) }}
                </div>
              </v-col>
              <v-col cols="6" md="3">
                <div class="label-info">DIABETES</div>
                <div class="text-body-1">
                  {{ traducirOpcion(paciente.fam_diabetes) }}
                </div>
              </v-col>
              <v-col cols="6" md="3">
                <div class="label-info">ASMA</div>
                <div class="text-body-1">
                  {{ traducirOpcion(paciente.fam_asma) }}
                </div>
              </v-col>
            </v-row>
          </section>

          <v-divider class="grey darken-4 mb-10"></v-divider>

          <section class="mb-10">
            <h3
              class="text-h5 font-weight-thin grey--text text--lighten-2 mb-5"
            >
              5. Constantes Físicas y Laboratorio
            </h3>
            <v-row class="mb-6">
              <v-col cols="6" md="2">
                <div class="label-info">ALTURA</div>
                <div class="text-body-1">{{ paciente.altura || "-" }} m</div>
              </v-col>
              <v-col cols="6" md="2">
                <div class="label-info">PESO</div>
                <div class="text-body-1">{{ paciente.peso || "-" }} Kg</div>
              </v-col>
              <v-col cols="6" md="2">
                <div class="label-info">PRESIÓN SISTÓLICA</div>
                <div class="text-body-1">
                  {{ paciente.presion_sistolica_final || "-" }} mmHg
                </div>
              </v-col>
              <v-col cols="6" md="2">
                <div class="label-info">PRESIÓN DIASTÓLICA</div>
                <div class="text-body-1">
                  {{ paciente.presion_diastolica_final || "-" }} mmHg
                </div>
              </v-col>
            </v-row>

            <v-row>
              <v-col
                v-for="lab in itemsLaboratorio"
                :key="lab.key"
                cols="6"
                md="3"
                class="mb-4"
              >
                <div class="label-info">{{ lab.label }}</div>
                <div class="text-body-1">
                  {{ paciente[lab.key] || "-" }}
                  <small class="grey--text text--darken-1">{{
                    lab.unit
                  }}</small>
                </div>
              </v-col>
            </v-row>
          </section>
          <div class="d-flex justify-center pt-6">
            <v-btn
              color="primary"
              x-large
              :to="{
                path: '/historial/analisis',
                query: {
                  dni: paciente.dni,
                  visitaId: paciente.id,
                },
              }"
            >
              <v-icon left>fas fa-chart-pie</v-icon>
              Ver Análisis de Riesgo e Influencias
            </v-btn>
          </div>
        </div>
      </v-sheet>
    </v-container>

    <FormularioPaciente
      v-else
      :datosIniciales="datosParaFormulario"
      :modoEdicion="true"
      @atras="mostrandoEdicion = false"
      @guardado="alGuardar"
    />
  </div>
</template>

<script>
import { pacienteService } from "@/services/pacienteService";
import FormularioPaciente from "@/components/FormularioPaciente.vue";

export default {
  components: { FormularioPaciente },
  data() {
    return {
      cargando: true,
      mostrandoEdicion: false,
      paciente: {},
      datosParaFormulario: null,
      itemsLaboratorio: [
        { label: "COLESTEROL TOTAL", key: "colesterol_total", unit: "mg/dL" },
        { label: "HDL", key: "hdl", unit: "mg/dL" },
        { label: "TRIGLICÉRIDOS", key: "trigliceridos", unit: "mg/dL" },
        { label: "PROT. C REACTIVA", key: "proteina_c", unit: "mg/L" },
        { label: "HEMOGLOBINA", key: "hemoglobina", unit: "g/dL" },
        { label: "CREATININA", key: "creatinina", unit: "mg/dL" },
        { label: "ÁCIDO ÚRICO", key: "acido_urico", unit: "mg/dL" },
        { label: "POTASIO", key: "potasio", unit: "mmol/L" },
      ],
    };
  },
  computed: {
    pacienteDni() {
      return this.$route.query.dni;
    },
    estaCompleto() {
      if (!this.paciente) return false;
      const obligatorios = [
        "altura",
        "peso",
        "presion_sistolica_final",
        "presion_diastolica_final",
        "colesterol_total",
        "hdl",
        "trigliceridos",
      ];
      return obligatorios.every(
        (f) =>
          this.paciente[f] !== null &&
          this.paciente[f] !== undefined &&
          this.paciente[f] !== ""
      );
    },
  },
  mounted() {
    if (this.pacienteDni) this.cargarDatosPaciente(this.pacienteDni);
  },
  methods: {
    async cargarDatosPaciente(dni) {
      this.cargando = true;
      try {
        const res = await pacienteService.buscarPorDni(dni);
        const p = Array.isArray(res) ? res[0] : res;

        if (p && p.visitas && p.visitas.length > 0) {
          // 1. Intentamos obtener el ID de la visita desde la URL (si es que lo pasas por query)
          const visitaIdDeUrl = this.$route.query.visitaId;

          let visitaSeleccionada;

          if (visitaIdDeUrl) {
            visitaSeleccionada = p.visitas.find((v) => v.id == visitaIdDeUrl);
          }

          if (!visitaSeleccionada) {
            visitaSeleccionada = p.visitas[p.visitas.length - 1];
          }

          this.paciente = { ...p, ...visitaSeleccionada };
        } else {
          this.paciente = p;
        }
      } catch (e) {
        console.error("Error al cargar datos:", e);
      } finally {
        this.cargando = false;
      }
    },
    irAEditar() {
      const mapeoValor = (v) => {
        if (v === 1.0) return "S";
        if (v === 2.0) return "N";
        if (v === 9.0) return "X";
        if (v === 3.0) return "P";
        return null;
      };

      this.datosParaFormulario = {
        ...this.paciente,
        id: this.paciente.id,
        apellido: this.paciente.apellido,
        nombre: this.paciente.nombre,
        dni: this.paciente.dni,
        edad: this.paciente.edad,
        genero: this.paciente.genero === 0 ? "Masculino" : "Femenino",
        genero: this.paciente.genero === 0 ? "Masculino" : "Femenino",
        diabetico: mapeoValor(this.paciente.diabetes),
        asma: mapeoValor(this.paciente.asma),
        hipertension: mapeoValor(this.paciente.hipertension),
        renales: mapeoValor(this.paciente.riñones_debiles_fallando),
        fumador: this.paciente.fumo_100_cigarrillos,
        alcohol: this.paciente.consumo_alcohol_ultimo_año,
        ejercicio: this.paciente.actividad_deportiva_moderada_x_semana,
        anhedonia: this.paciente.anhedonia,
        fam_cardio: mapeoValor(this.paciente.fam_cardio),
        fam_diabetes: mapeoValor(this.paciente.fam_diabetes),
        fam_asma: mapeoValor(this.paciente.fam_asma),
        presion_sis: this.paciente.presion_sistolica_final,
        presion_dis: this.paciente.presion_diastolica_final,
        colesterol: this.paciente.colesterol_total,
        pcr: this.paciente.proteina_c,
      };

      this.mostrandoEdicion = true;
    },
    async alGuardar() {
      this.mostrandoEdicion = false;
      await this.cargarDatosPaciente(this.pacienteDni);
    },
    traducirOpcion(val, tipo = "comun") {
      const n = parseFloat(val);
      if (tipo === "diabetes" && n === 3.0) return "PREDIABETES";
      if (n === 1.0) return "SÍ";
      if (n === 2.0) return "NO";
      if (n === 9.0) return "NO SABE";
      return "-";
    },
    traducirGenero(val) {
      const n = parseFloat(val);
      return n === 0.0 ? "Masculino" : n === 1.0 ? "Femenino" : "-";
    },
    traducirAlcohol(val) {
      const opciones = {
        0: "Nunca",
        10: "Diariamente",
        9: "Casi diario",
        8: "3-4 veces por semana",
        7: "2 veces por semana",
        6: "Una vez por semana",
        5: "2-3 veces por mes",
        4: "Una vez al mes",
        3: "7-11 veces al año",
        2: "3-6 veces al año",
        1: "1-2 veces al año",
      };
      return opciones[val] || "-";
    },
    traducirBinario(val) {
      if (val === 1 || val === 1.0) return "SÍ";
      if (val === 0 || val === 0.0) return "NO";
      return "-";
    },
    traducirAnhedonia(val) {
      const opciones = {
        0: "Nunca",
        1: "Varios días",
        2: "Más de la mitad de los días",
        3: "Casi todos los días",
      };
      return opciones[val] || "-";
    },
    formatearFecha(f) {
      return f ? new Date(f).toLocaleDateString("es-AR") : "-";
    },
  },
};
</script>

<style scoped>
.label-info {
  color: #616161;
  font-size: 0.75rem;
  font-weight: 700;
  margin-bottom: 2px;
  text-transform: uppercase;
}
.custom-scroll-area::-webkit-scrollbar {
  width: 8px;
}
.custom-scroll-area::-webkit-scrollbar-thumb {
  background: #333;
  border-radius: 4px;
}
</style>
