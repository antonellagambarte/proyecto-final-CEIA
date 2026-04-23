<template>
  <v-container
    class="pa-0 d-flex flex-column shadow-none"
    fluid
    style="
      height: calc(100vh - 64px - 36px);
      background-color: #1a1a1a;
      overflow: hidden;
    "
  >
    <v-dialog v-model="modalConfirmacion" max-width="450" persistent>
      <v-card color="#2a2a2a" class="pa-4 text-center border-grey">
        <v-icon color="warning" size="64" class="mb-4"
          >fas fa-exclamation-triangle</v-icon
        >
        <v-card-title class="white--text justify-center text-h5"
          >¿Confirmar Guardado?</v-card-title
        >
        <v-card-text class="grey--text text--lighten-1">
          Una vez guardados, los datos del paciente
          <strong class="white--text">quedarán bloqueados</strong> para asegurar
          la integridad de la historia clínica.
        </v-card-text>
        <v-card-actions class="justify-center mt-2">
          <v-btn
            text
            color="grey lighten-1"
            class="px-6 custom-btn"
            @click="modalConfirmacion = false"
            >CANCELAR</v-btn
          >
          <v-btn
            color="success"
            class="px-6 custom-btn"
            @click="confirmarGuardado"
            >SÍ, GUARDAR</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="modalExito" max-width="400" persistent>
      <v-card color="#2a2a2a" class="pa-4 text-center border-grey">
        <v-icon
          :color="
            resultadoIA
              ? resultadoIA.riesgo === 'Alto'
                ? 'error'
                : 'success'
              : 'success'
          "
          size="64"
          class="mb-4"
        >
          {{ resultadoIA ? "fas fa-chart-line" : "fas fa-check-circle" }}
        </v-icon>
        <v-card-title class="white--text justify-center text-h5">
          {{ resultadoIA ? "Resultado de Riesgo" : "¡Guardado con éxito!" }}
        </v-card-title>
        <v-card-text class="grey--text text--lighten-1 text-center">
          <div
            v-if="resultadoIA"
            class="mt-2 pa-4 rounded-lg"
            :class="
              resultadoIA.riesgo === 'Alto' ? 'red darken-4' : 'green darken-4'
            "
          >
            <div class="white--text text-overline mb-1">
              Probabilidad de riesgo (Etapa {{ resultadoIA.etapa_aplicada }})
            </div>
            <div class="white--text text-h4 font-weight-black">
              RIESGO {{ resultadoIA.riesgo.toUpperCase() }}
            </div>
          </div>
          <div v-else>Los datos han sido sincronizados correctamente.</div>
        </v-card-text>
        <v-card-actions class="justify-center mt-2 pb-4">
          <v-btn
            v-if="resultadoIA"
            text
            color="info"
            class="px-6 custom-btn"
            @click="irADetallePrediccion"
            >VER DETALLE</v-btn
          >
          <v-btn
            color="success"
            class="px-10 custom-btn ml-2"
            @click="cerrarModal"
            >ACEPTAR</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-sheet color="transparent" width="100%" class="pa-6 pb-0 flex-shrink-0">
      <div
        class="d-flex align-center cursor-pointer"
        @click="manejarAtras"
        style="width: fit-content"
      >
        <v-icon small color="grey lighten-1">fas fa-arrow-left</v-icon>
        <span class="grey--text text--lighten-1 caption ml-2">
          {{
            modoEdicion
              ? "Volver al historial"
              : paso === 1
              ? "Volver a búsqueda"
              : "Nuevo paciente"
          }}
        </span>
      </div>
    </v-sheet>

    <v-sheet
      color="transparent"
      width="100%"
      class="px-12 pt-8 flex-grow-1 d-flex flex-column"
      style="overflow-y: auto; min-height: 0"
    >
      <v-card flat color="transparent" width="100%" max-width="1200">
        <h2 class="white--text text-h4 mb-8 font-weight-light">
          {{ titulos[paso - 1] }}
        </h2>
        <v-form ref="form" v-model="formValido">
          <div v-if="paso === 1">
            <v-row dense class="mb-4">
              <v-col cols="12" md="5">
                <p class="custom-label">Apellido *</p>
                <v-text-field
                  v-model="form.apellido"
                  solo
                  dark
                  dense
                  hide-details="auto"
                  background-color="#4a4444"
                  :readonly="esCampoBloqueado('apellido')"
                  :class="{ 'input-bloqueado': esCampoBloqueado('apellido') }"
                  :rules="[(v) => !!v || 'Requerido']"
                />
              </v-col>
              <v-col cols="12" md="5" offset-md="1">
                <p class="custom-label">Nombre *</p>
                <v-text-field
                  v-model="form.nombre"
                  solo
                  dark
                  dense
                  hide-details="auto"
                  background-color="#4a4444"
                  :readonly="esCampoBloqueado('nombre')"
                  :class="{ 'input-bloqueado': esCampoBloqueado('nombre') }"
                  :rules="[(v) => !!v || 'Requerido']"
                />
              </v-col>
            </v-row>
            <v-row dense class="mb-6">
              <v-col cols="12" md="4">
                <p class="custom-label">Género *</p>
                <v-select
                  v-model="form.genero"
                  :items="['Masculino', 'Femenino']"
                  solo
                  dark
                  dense
                  hide-details="auto"
                  background-color="#4a4444"
                  :readonly="esCampoBloqueado('genero')"
                  :class="{ 'input-bloqueado': esCampoBloqueado('genero') }"
                  :rules="[(v) => !!v || 'Requerido']"
                />
              </v-col>
              <v-col cols="12" md="3" offset-md="1">
                <p class="custom-label">DNI *</p>
                <v-text-field
                  v-model="form.dni"
                  solo
                  dark
                  dense
                  hide-details="auto"
                  background-color="#4a4444"
                  :readonly="esCampoBloqueado('dni')"
                  :class="{ 'input-bloqueado': esCampoBloqueado('dni') }"
                  :rules="[(v) => !!v || 'Requerido']"
                />
              </v-col>
              <v-col cols="12" md="2" offset-md="1">
                <p class="custom-label">Edad *</p>
                <v-text-field
                  v-model="form.edad"
                  solo
                  dark
                  dense
                  hide-details="auto"
                  background-color="#4a4444"
                  :readonly="esCampoBloqueado('edad')"
                  :class="{ 'input-bloqueado': esCampoBloqueado('edad') }"
                  :rules="[(v) => !!v || 'Requerido']"
                />
              </v-col>
            </v-row>
            <v-divider class="grey darken-3 mb-6"></v-divider>
            <h3 class="white--text text-h5 mb-6 font-weight-light">
              Antecedentes médicos *
            </h3>
            <v-row dense>
              <v-col
                cols="12"
                md="3"
                v-for="(item, idx) in antecedentesMedicos"
                :key="idx"
              >
                <p class="custom-label">{{ item.label }}</p>
                <v-select
                  v-model="form[item.key]"
                  :items="item.options"
                  item-text="text"
                  item-value="value"
                  solo
                  dark
                  dense
                  hide-details="auto"
                  background-color="#4a4444"
                  :readonly="esCampoBloqueado(item.key)"
                  :class="{ 'input-bloqueado': esCampoBloqueado(item.key) }"
                  :rules="[(v) => v !== null || 'Requerido']"
                />
              </v-col>
            </v-row>
          </div>

          <div v-if="paso === 2">
            <v-row v-for="(q, i) in preguntasVida" :key="i" dense class="mb-5">
              <v-col cols="12" md="10">
                <p class="custom-label">{{ q.label }} *</p>
                <v-select
                  v-model="form[q.key]"
                  :items="q.options"
                  item-text="text"
                  item-value="value"
                  solo
                  dark
                  dense
                  hide-details="auto"
                  background-color="#4a4444"
                  :readonly="esCampoBloqueado(q.key)"
                  :class="{ 'input-bloqueado': esCampoBloqueado(q.key) }"
                  :rules="[(v) => v !== null || 'Requerido']"
                />
              </v-col>
            </v-row>
          </div>

          <div v-if="paso === 3">
            <v-row dense class="mb-4">
              <v-col
                cols="12"
                md="5"
                v-for="ant in antecedentesFamiliaresConfig"
                :key="ant.key"
                class="mb-4"
              >
                <p class="custom-label">{{ ant.label }} *</p>
                <v-select
                  v-model="form[ant.key]"
                  :items="itemsCompletos"
                  item-text="text"
                  item-value="value"
                  solo
                  dark
                  dense
                  hide-details="auto"
                  background-color="#4a4444"
                  :readonly="esCampoBloqueado(ant.key)"
                  :class="{ 'input-bloqueado': esCampoBloqueado(ant.key) }"
                  :rules="[(v) => v !== null || 'Requerido']"
                />
              </v-col>
            </v-row>
            <v-divider class="grey darken-3 mb-6"></v-divider>
            <h3 class="white--text text-h5 mb-4 font-weight-light">
              Evaluación física *
            </h3>
            <v-row dense>
              <v-col
                cols="6"
                md="3"
                v-for="itemF in evaluacionFisicaConfig"
                :key="itemF.key"
              >
                <p class="custom-label">{{ itemF.label }}</p>
                <v-text-field
                  v-model="form[itemF.key]"
                  solo
                  dark
                  dense
                  hide-details="auto"
                  background-color="#4a4444"
                  :readonly="esCampoBloqueado(itemF.key)"
                  :class="{ 'input-bloqueado': esCampoBloqueado(itemF.key) }"
                  :rules="[(v) => !!v || 'Requerido']"
                />
              </v-col>
            </v-row>
          </div>

          <div v-if="paso === 4">
            <div v-for="(sec, sIdx) in laboratorio" :key="sIdx">
              <h4
                class="white--text subtitle-2 mb-3 grey--text text--lighten-1"
              >
                {{ sec.titulo }}
              </h4>
              <v-row dense class="mb-4">
                <v-col
                  v-for="campo in sec.campos"
                  :key="campo.key"
                  cols="12"
                  md="4"
                >
                  <p class="custom-label">{{ campo.label }}</p>
                  <v-text-field
                    v-model="form[campo.key]"
                    solo
                    dark
                    dense
                    hide-details
                    background-color="#4a4444"
                    :readonly="esCampoBloqueado(campo.key)"
                    :class="{ 'input-bloqueado': esCampoBloqueado(campo.key) }"
                  />
                </v-col>
              </v-row>
              <v-divider
                v-if="sIdx < laboratorio.length - 1"
                class="grey darken-3 mb-6"
              ></v-divider>
            </div>
          </div>
        </v-form>
      </v-card>
    </v-sheet>

    <v-sheet color="transparent" width="100%" class="pa-10 flex-shrink-0">
      <v-row no-gutters justify="end" align="center">
        <v-btn
          v-if="form.id"
          color="info"
          outlined
          class="mr-4 custom-btn"
          @click="$router.push(`/historial/${form.dni}`)"
        >
          <v-icon left small>fas fa-history</v-icon> VER HISTORIAL
        </v-btn>
        <v-btn
          v-if="mostrarBotonGuardar"
          color="success"
          outlined
          class="mr-4 custom-btn"
          @click="guardarCambios"
        >
          <v-icon left small>fas fa-save</v-icon> GUARDAR DATOS
        </v-btn>
        <v-btn
          v-if="paso >= 3"
          color="success"
          class="mr-4 custom-btn"
          @click="predecir"
        >
          <v-icon left small>fas fa-chart-line</v-icon> PREDICCIÓN
          {{ paso === 3 ? "PRELIMINAR" : "FINAL" }}
        </v-btn>
        <v-btn
          v-if="paso < 4"
          color="#635b5b"
          class="white--text custom-btn px-10"
          @click="siguiente"
          >SIGUIENTE</v-btn
        >
      </v-row>
    </v-sheet>
  </v-container>
</template>

<script>
import { pacienteService } from "~/services/pacienteService";
import {
  OpcionesCompletas,
  OpcionesDiabetes,
  OpcionesAlcohol,
  OpcionesAnhedonia,
} from "~/constants/opciones";

export default {
  props: {
    datosIniciales: { type: Object, default: () => ({}) },
    modoEdicion: { type: Boolean, default: false },
  },
  data() {
    return {
      modalExito: false,
      modalConfirmacion: false,
      resultadoIA: null,
      paso: 1,
      formValido: false,
      bloqueoEdicion: this.modoEdicion,
      form: this.inicializarForm(),
      camposPersistidos: [],
      itemsCompletos: [
        { text: "Sí", value: OpcionesCompletas.SI },
        { text: "No", value: OpcionesCompletas.NO },
        { text: "No sabe", value: OpcionesCompletas.NO_SABE },
      ],
      itemsDiabetes: [
        { text: "Sí", value: OpcionesDiabetes.SI },
        { text: "No", value: OpcionesDiabetes.NO },
        { text: "No sabe", value: OpcionesDiabetes.NO_SABE },
        { text: "Prediabetes", value: OpcionesDiabetes.PREDIABETES },
      ],
      titulos: [
        "Datos personales",
        "Estilo de vida",
        "Antecedentes familiares",
        "Resultados de laboratorio",
      ],
      antecedentesMedicos: [],
      preguntasVida: [],
      antecedentesFamiliaresConfig: [
        { key: "fam_cardio", label: "Enfermedad cardiovascular" },
        { key: "fam_diabetes", label: "Diabetes" },
        { key: "fam_asma", label: "Asma" },
      ],
      evaluacionFisicaConfig: [
        { key: "altura", label: "Altura (m)" },
        { key: "peso", label: "Peso (Kg)" },
        { key: "presion_sis", label: "Presión sistólica" },
        { key: "presion_dis", label: "Presión diastólica" },
      ],
      laboratorio: [
        {
          titulo: "Perfil lipídico",
          campos: [
            { key: "colesterol", label: "Colesterol total" },
            { key: "hdl", label: "HDL" },
            { key: "trigliceridos", label: "Triglicéridos" },
          ],
        },
        {
          titulo: "Función renal",
          campos: [
            { key: "creatinina", label: "Creatinina" },
            { key: "pcr", label: "Proteína C (PCR)" },
          ],
        },
        {
          titulo: "Hematología",
          campos: [
            { key: "hemoglobina", label: "Hemoglobina" },
            { key: "acido_urico", label: "Ácido úrico" },
            { key: "potasio", label: "Potasio" },
          ],
        },
      ],
    };
  },
  computed: {
    pasoLabGuardado() {
      const keysLab = this.laboratorio.flatMap((s) =>
        s.campos.map((c) => c.key)
      );
      return keysLab.every((key) => this.camposPersistidos.includes(key));
    },
    mostrarBotonGuardar() {
      if (this.paso < 3) return false;
      if (this.paso === 4) return !this.pasoLabGuardado;
      return !this.bloqueoEdicion;
    },
  },
  created() {
    this.antecedentesMedicos = [
      {
        key: "diabetico",
        label: "¿Es diabético?",
        options: this.itemsDiabetes,
      },
      {
        key: "hipertension",
        label: "¿Es hipertenso?",
        options: this.itemsCompletos,
      },
      { key: "asma", label: "¿Es asmático?", options: this.itemsCompletos },
      {
        key: "renales",
        label: "¿Problemas renales?",
        options: this.itemsCompletos,
      },
    ];
    this.preguntasVida = [
      {
        key: "alcohol",
        label: "Frecuencia de consumo de alcohol",
        options: this.getAlcoholOptions(),
      },
      {
        key: "ejercicio",
        label: "Días de actividad física",
        options: Array.from({ length: 8 }, (_, i) => ({
          text: `${i} días`,
          value: i,
        })),
      },
      {
        key: "fumador",
        label: "¿Ha fumado al menos 100 cigarrillos?",
        options: this.itemsCompletos,
      },
      {
        key: "anhedonia",
        label: "Presencia de Anhedonia",
        options: this.getAnhedoniaOptions(),
      },
    ];
  },
  watch: {
    datosIniciales: {
      handler(newVal) {
        if (newVal && Object.keys(newVal).length > 0) {
          console.log("NUEVO VALOR: ", newVal);

          this.form = { ...this.form, ...newVal };
          this.camposPersistidos = Object.keys(newVal).filter(
            (k) => newVal[k] !== null && newVal[k] !== "" && k !== "id"
          );
        }
      },
      immediate: true,
      deep: true,
    },
  },
  methods: {
    esCampoBloqueado(campo) {
      return this.camposPersistidos.includes(campo);
    },
    async guardarCambios() {
      if (this.$refs.form.validate()) this.modalConfirmacion = true;
    },
    async confirmarGuardado() {
      this.modalConfirmacion = false;
      try {
        const res = await pacienteService.guardar(this.prepararPayload());
        if (res?.id) {
          this.form.id = res.id;
          this.modalExito = true;
        }
      } catch (e) {
        console.error(e);
      }
    },
    async predecir() {
      if (!this.$refs.form.validate()) return;
      try {
        const res = await pacienteService.predecirAlVuelo(
          this.prepararPayload()
        );
        this.resultadoIA = res;
        this.modalExito = true;
      } catch (e) {
        console.error(e);
      }
    },
    prepararPayload() {
      // Mapa de conversión estricta a Float para el modelo/backend
      const mapa = (v) => {
        if (v === "S") return 1.0;
        if (v === "N") return 2.0;
        if (v === "P") return 3.0; // Prediabetes
        if (v === "X") return 9.0; // No sabe
        return null;
      };

      return {
        // Datos identificatorios
        id: this.form.id,
        dni: this.form.dni,
        nombre: this.form.nombre,
        apellido: this.form.apellido,

        // Conversiones numéricas obligatorias
        edad: parseInt(this.form.edad) || 0,
        genero: this.form.genero === "Masculino" ? 0.0 : 1.0,

        // Mapeo de selectores (String -> Float)
        // Usamos las claves que espera tu backend según el JSON que pasaste
        fumo_100_cigarrillos: mapa(this.form.fumador),
        riñones_debiles_fallando: mapa(this.form.renales),
        diabetes: mapa(this.form.diabetico),
        hipertension: mapa(this.form.hipertension),
        asma: mapa(this.form.asma),

        // Antecedentes familiares
        fam_cardio: mapa(this.form.fam_cardio),
        fam_diabetes: mapa(this.form.fam_diabetes),
        fam_asma: mapa(this.form.fam_asma),

        // Estilo de vida (Ya son numéricos por las constantes OpcionesAlcohol/Anhedonia)
        consumo_alcohol_ultimo_año: this.form.alcohol,
        actividad_deportiva_moderada_x_semana: this.form.ejercicio,
        anhedonia: this.form.anhedonia,

        // Medidas físicas (Siempre Float)
        altura: parseFloat(this.form.altura) || null,
        peso: parseFloat(this.form.peso) || null,
        presion_sistolica_final: parseFloat(this.form.presion_sis) || null,
        presion_diastolica_final: parseFloat(this.form.presion_dis) || null,

        // Laboratorio (Blindaje contra nulos o strings vacíos)
        colesterol_total: this.form.colesterol
          ? parseFloat(this.form.colesterol)
          : null,
        hdl: this.form.hdl ? parseFloat(this.form.hdl) : null,
        trigliceridos: this.form.trigliceridos
          ? parseFloat(this.form.trigliceridos)
          : null,
        creatinina: this.form.creatinina
          ? parseFloat(this.form.creatinina)
          : null,
        proteina_c: this.form.pcr ? parseFloat(this.form.pcr) : null,
        hemoglobina: this.form.hemoglobina
          ? parseFloat(this.form.hemoglobina)
          : null,
        acido_urico: this.form.acido_urico
          ? parseFloat(this.form.acido_urico)
          : null,
        potasio: this.form.potasio ? parseFloat(this.form.potasio) : null,
      };
    },
    siguiente() {
      if (this.$refs.form.validate()) this.paso++;
    },
    manejarAtras() {
      this.paso > 1 ? this.paso-- : this.$emit("atras");
    },
    cerrarModal() {
      this.modalExito = false;
      if (this.paso === 4 && this.pasoLabGuardado) this.$emit("finalizar");
    },
    inicializarForm() {
      return {
        id: null,
        apellido: "",
        nombre: "",
        genero: null,
        dni: "",
        edad: null,
        diabetico: null,
        hipertension: null,
        asma: null,
        renales: null,
        alcohol: null,
        ejercicio: null,
        fumador: null,
        anhedonia: null,
        fam_cardio: null,
        fam_diabetes: null,
        fam_asma: null,
        altura: null,
        peso: null,
        presion_sis: null,
        presion_dis: null,
        colesterol: null,
        hdl: null,
        trigliceridos: null,
        creatinina: null,
        pcr: null,
        hemoglobina: null,
        acido_urico: null,
        potasio: null,
      };
    },
    getAlcoholOptions() {
      return [
        { text: "Nunca", value: OpcionesAlcohol.NUNCA },
        { text: "Diariamente", value: OpcionesAlcohol.DIARIAMENTE },
        { text: "Casi diario", value: OpcionesAlcohol.CASI_DIARIO },
        {
          text: "3-4 veces x semana",
          value: OpcionesAlcohol.TRES_CUATRO_SEMANA,
        },
        { text: "2 veces x semana", value: OpcionesAlcohol.DOS_VECES_SEMANA },
        { text: "Una vez x semana", value: OpcionesAlcohol.UNA_VEZ_SEMANA },
        { text: "2-3 veces x mes", value: OpcionesAlcohol.DOS_TRES_MES },
        { text: "Una vez al mes", value: OpcionesAlcohol.UNA_VEZ_MES },
        { text: "No sabe", value: OpcionesAlcohol.NO_SABE },
      ];
    },
    getAnhedoniaOptions() {
      return [
        { text: "Para nada", value: OpcionesAnhedonia.NADA },
        { text: "Varios días", value: OpcionesAnhedonia.VARIOS_DIAS },
        { text: "Más de la mitad", value: OpcionesAnhedonia.MAS_DE_LA_MITAD },
        { text: "Casi todos los días", value: OpcionesAnhedonia.CASI_DIARIO },
        { text: "No sabe", value: OpcionesAnhedonia.NO_SABE },
      ];
    },
    irADetallePrediccion() {
      this.modalExito = false;
      this.$router.push(`/historial/prediccion/${this.form.dni}`);
    },
  },
};
</script>

<style scoped>
.custom-label {
  color: #ffffff;
  font-size: 0.85rem;
  font-weight: 300;
  margin-bottom: 4px;
}
.custom-btn {
  height: 42px !important;
  font-size: 0.75rem;
  font-weight: bold;
}
.border-grey {
  border: 1px solid #4a4a4a !important;
}
.input-bloqueado {
  opacity: 0.7;
  filter: grayscale(0.4);
  pointer-events: none;
  background-color: #333 !important;
}
</style>
