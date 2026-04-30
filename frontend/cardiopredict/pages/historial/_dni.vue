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
        @click="$router.push('/historial')"
      >
        <v-icon small color="grey">fas fa-arrow-left</v-icon>
        <span class="grey--text caption ml-2 cursor-pointer"
          >Volver a búsqueda</span
        >
      </div>

      <h2 class="white--text text-h4 mb-8 font-weight-light">
        Historial: {{ paciente.apellido }}, {{ paciente.nombre }}
      </h2>

      <v-row class="grey--text text--caption mb-2 px-4 font-weight-bold">
        <v-col cols="2">Fecha Inicio</v-col>
        <v-col cols="2">Última Modif.</v-col>
        <v-col cols="2">Estado</v-col>
        <v-col cols="6" class="text-right">
          <v-btn
            color="#43a047"
            class="black--text custom-btn-new"
            elevation="2"
            small
            @click="nuevaVisita"
          >
            <v-icon left x-small>fas fa-plus</v-icon>
            <span class="black--text"> NUEVA VISITA </span>
          </v-btn>
        </v-col>
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
            class="black--text custom-btn"
            small
            :to="`/historial/datos?dni=${item.dni}&visitaId=${item.id}`"
          >
            VER DATOS
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
        // 1. Obtenemos el objeto paciente (el primero si es un array)
        const pacienteData = Array.isArray(res) ? res[0] : res;

        if (!pacienteData) return;

        const inversoMapa = (v) => {
          if (v === 1.0) return "S";
          if (v === 2.0) return "N";
          if (v === 9.0) return "X";
          if (v === 3.0) return "P";
          return null;
        };

        // 2. Mapeamos las VISITAS del paciente, no el paciente en sí
        this.historial = pacienteData.visitas.map((v) => ({
          // Mantenemos los datos del paciente para que los botones de VER DATOS funcionen
          dni: pacienteData.dni,
          nombre: pacienteData.nombre,
          apellido: pacienteData.apellido,

          // Datos de la visita (ID, campos clínicos y FECHAS)
          ...v,
          genero: v.genero === 0 ? "Masculino" : "Femenino",
          diabetico: inversoMapa(v.diabetes),
          hipertension: inversoMapa(v.hipertension),
          asma: inversoMapa(v.asma),
          renales: inversoMapa(v.riñones_debiles_fallando),

          alcohol: v.consumo_alcohol_ultimo_año,
          ejercicio: v.actividad_deportiva_moderada_x_semana,
          fumador: v.fumo_100_cigarrillos,
          anhedonia: v.anhedonia,

          fam_cardio: inversoMapa(v.fam_cardio),
          fam_diabetes: inversoMapa(v.fam_diabetes),
          fam_asma: inversoMapa(v.fam_asma),

          presion_sis: v.presion_sistolica_final,
          presion_dis: v.presion_diastolica_final,
          colesterol: v.colesterol_total,
          pcr: v.proteina_c,

          // IMPORTANTE: Ahora usamos las fechas de la VISITA
          fecha_creacion: v.fecha_visita,
          fecha_actualizacion: v.fecha_actualizacion,
        }));

        // 3. Ordenar por fecha de creación de la visita (de más reciente a más antigua)
        if (this.historial.length > 0) {
          this.historial.sort(
            (a, b) => new Date(b.fecha_creacion) - new Date(a.fecha_creacion)
          );

          // Seteamos el nombre del paciente para la cabecera
          this.paciente = {
            apellido: pacienteData.apellido,
            nombre: pacienteData.nombre,
          };
        }
      } catch (error) {
        console.error("Error al cargar historial:", error);
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
      this.$router.push({
        path: "/historial/analisis",
        query: {
          visitaId: item.id,
          dni: item.dni,
        },
      });
    },

    nuevaVisita() {
      this.$router.push({
        path: "/nuevo-paciente",
        query: {
          dni: this.dni,
          nombre: this.paciente.nombre,
          apellido: this.paciente.apellido,
          genero: this.historial[0].genero,
        },
      });
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

.custom-btn-new {
  font-size: 0.7rem !important;
  font-weight: bold;
  letter-spacing: 1px;
  border-radius: 4px; /* O 8px si prefieres bordes más redondeados */
}

.cursor-pointer {
  cursor: pointer;
}
</style>
