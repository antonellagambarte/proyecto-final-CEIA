<template>
  <div>
    <v-container
      v-if="loading"
      fluid
      class="pa-12 d-flex justify-center align-center"
      style="background-color: #1a1a1a; min-height: 100vh"
    >
      <v-progress-circular indeterminate color="grey"></v-progress-circular>
    </v-container>

    <v-container
      v-else-if="!verDetalleForm"
      fluid
      class="pa-12"
      style="background-color: #1a1a1a; min-height: 100vh"
    >
      <div
        class="d-flex align-center mb-6 cursor-pointer"
        @click="$router.back()"
      >
        <v-icon small color="grey">fas fa-arrow-left</v-icon>
        <span class="grey--text caption ml-2">Volver a búsqueda</span>
      </div>

      <h2 class="white--text text-h4 mb-8 font-weight-light">
        Historial: {{ paciente.apellido }}, {{ paciente.nombre }}
      </h2>

      <v-row class="grey--text text--caption mb-2 px-4 font-weight-bold">
        <v-col cols="2">Fecha Inicio</v-col>
        <v-col cols="2">Última Modif.</v-col>
        <v-col cols="2">Estado</v-col>
        <v-col cols="6"></v-col>
      </v-row>
      <v-divider class="grey darken-3 mb-4"></v-divider>

      <v-row
        v-for="(item, i) in historial"
        :key="i"
        class="white--text align-center py-4 px-4 border-bottom"
      >
        <v-col cols="2" class="body-2">
          {{ formatearFecha(item.fecha_creacion) }}
        </v-col>
        <v-col cols="2" class="grey--text caption">
          {{
            item.fecha_actualizacion
              ? formatearFecha(item.fecha_actualizacion)
              : "-"
          }}
        </v-col>
        <v-col cols="2">
          <v-chip small :color="obtenerEstado(item).color" outlined>
            {{ obtenerEstado(item).texto }}
          </v-chip>
        </v-col>
        <v-col cols="6" class="text-right">
          <v-btn
            outlined
            color="#a39a9a"
            class="mr-4 custom-btn"
            small
            @click="verPrediccion(item)"
          >
            VER PREDICCIÓN
          </v-btn>
          <v-btn
            color="#635b5b"
            class="white--text custom-btn"
            small
            @click="irADetalle(item)"
          >
            VER / COMPLETAR DATOS
          </v-btn>
        </v-col>
      </v-row>
    </v-container>

    <FormularioPaciente
      v-else
      :datosIniciales="pacienteSeleccionado"
      :modoEdicion="true"
      @atras="verDetalleForm = false"
    />
  </div>
</template>

<script>
import FormularioPaciente from "@/components/FormularioPaciente.vue";
import { pacienteService } from "@/services/pacienteService";

export default {
  components: { FormularioPaciente },
  data() {
    return {
      loading: true,
      verDetalleForm: false,
      paciente: { apellido: "", nombre: "" },
      pacienteSeleccionado: null,
      historial: [],
      dni: this.$route.params.dni,
    };
  },
  methods: {
    async cargarPaciente() {
      this.loading = true;
      try {
        const res = await pacienteService.buscarPorDni(this.dni);
        const dataArray = Array.isArray(res) ? res : [res];

        const inversoMapa = (v) => {
          if (v === 1.0) return "S";
          if (v === 2.0) return "N";
          if (v === 9.0) return "X";
          if (v === 3.0) return "P";
          return null;
        };

        this.historial = dataArray.map((data) => ({
          ...data,
          genero: data.genero === 0 ? "Masculino" : "Femenino",
          diabetico: inversoMapa(data.diabetes),
          hipertension: inversoMapa(data.hipertension),
          renales: inversoMapa(data.riñones_debiles_fallando),

          alcohol: data.consumo_alcohol_ultimo_año,
          ejercicio: data.actividad_deportiva_moderada_x_semana,
          fumador: inversoMapa(data.fumo_100_cigarrillos),
          anhedonia: data.anhedonia,

          fam_cardio: inversoMapa(data.fam_cardio),
          fam_diabetes: inversoMapa(data.fam_diabetes),
          fam_asma: inversoMapa(data.fam_asma),

          presion_sis: data.presion_sistolica_final,
          presion_dis: data.presion_diastolica_final,
          colesterol: data.colesterol_total,
          pcr: data.proteina_c,
          fecha_creacion: data.fecha_creacion,
          fecha_actualizacion: data.fecha_actualizacion,
        }));

        if (this.historial.length > 0) {
          this.historial.sort(
            (a, b) => new Date(b.fecha_creacion) - new Date(a.fecha_creacion)
          );
          this.paciente = {
            apellido: this.historial[0].apellido,
            nombre: this.historial[0].nombre,
          };
        }
      } catch (error) {
        console.error("Error:", error);
      } finally {
        this.loading = false;
      }
    },
    obtenerEstado(item) {
      const completo = item.creatinina !== null && item.colesterol !== null;
      return completo
        ? { texto: "COMPLETO", color: "success" }
        : { texto: "PARCIAL", color: "warning" };
    },
    formatearFecha(fecha) {
      if (!fecha) return "-";
      const d = new Date(fecha);
      return d.toLocaleDateString("es-AR", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
      });
    },
    irADetalle(item) {
      this.pacienteSeleccionado = item;
      this.verDetalleForm = true;
    },
    verPrediccion(item) {
      const riesgo = (item.probabilidad_riesgo * 100).toFixed(2);
      alert(`Riesgo Cardiovascular calculado: ${riesgo}%`);
    },
  },
  async mounted() {
    await this.cargarPaciente();
  },
};
</script>

<style scoped>
.border-bottom {
  border-bottom: 1px solid #333 !important;
}
.custom-btn {
  font-size: 0.65rem !important;
  letter-spacing: 0.5px;
}
</style>
