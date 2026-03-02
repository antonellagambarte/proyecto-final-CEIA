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
    <v-sheet color="transparent" width="100%" class="pa-6 pb-0 flex-shrink-0">
      <div
        class="d-flex align-center cursor-pointer"
        @click="manejarAtras"
        style="width: fit-content"
      >
        <v-icon small color="grey lighten-1">fas fa-arrow-left</v-icon>
        <span class="grey--text text--lighten-1 caption ml-2">
          {{ modoEdicion ? "Volver al historial" : "Nuevo paciente" }}
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

        <v-form ref="form">
          <div v-if="paso === 1">
            <v-row dense class="mb-4">
              <v-col cols="12" md="5">
                <p class="custom-label">Apellido</p>
                <v-text-field
                  v-model="form.apellido"
                  solo
                  background-color="#4a4444"
                  dark
                  hide-details
                  dense
                  placeholder="Ingrese apellido"
                  :readonly="!bloqueoEdicion"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="5" offset-md="1">
                <p class="custom-label">Nombre</p>
                <v-text-field
                  v-model="form.nombre"
                  solo
                  background-color="#4a4444"
                  dark
                  hide-details
                  dense
                  placeholder="Ingrese nombre"
                  :readonly="!bloqueoEdicion"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row dense class="mb-6">
              <v-col cols="12" md="4">
                <p class="custom-label">Género</p>
                <v-select
                  v-model="form.genero"
                  :items="['Masculino', 'Femenino']"
                  placeholder="Seleccione una opción"
                  solo
                  background-color="#4a4444"
                  dark
                  hide-details
                  dense
                  :readonly="!bloqueoEdicion"
                ></v-select>
              </v-col>
              <v-col cols="12" md="3" offset-md="1">
                <p class="custom-label">DNI</p>
                <v-text-field
                  v-model="form.dni"
                  solo
                  background-color="#4a4444"
                  dark
                  hide-details
                  dense
                  placeholder="Ej: 40123456"
                  :readonly="!bloqueoEdicion"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="2" offset-md="1">
                <p class="custom-label">Edad</p>
                <v-text-field
                  v-model="form.edad"
                  solo
                  background-color="#4a4444"
                  dark
                  hide-details
                  dense
                  placeholder="0"
                  :readonly="!bloqueoEdicion"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-divider class="grey darken-3 mb-6"></v-divider>
            <h3 class="white--text text-h5 mb-6 font-weight-light">
              Antecedentes médicos
            </h3>
            <v-row dense>
              <v-col cols="12" md="5" class="mb-3">
                <p class="custom-label">¿Es diabético?</p>
                <v-select
                  v-model="form.diabetico"
                  :items="itemsDiabetes"
                  item-text="text"
                  item-value="value"
                  placeholder="Seleccione una opción"
                  solo
                  background-color="#4a4444"
                  dark
                  hide-details
                  dense
                  :readonly="!bloqueoEdicion"
                ></v-select>
              </v-col>
              <v-col cols="12" md="5" offset-md="1" class="mb-3">
                <p class="custom-label">¿Tiene problemas renales?</p>
                <v-select
                  v-model="form.renales"
                  :items="itemsCompletos"
                  item-text="text"
                  item-value="value"
                  placeholder="Seleccione una opción"
                  solo
                  background-color="#4a4444"
                  dark
                  hide-details
                  dense
                  :readonly="!bloqueoEdicion"
                ></v-select>
              </v-col>
            </v-row>
          </div>

          <div v-if="paso === 2">
            <v-row v-for="(q, i) in preguntasVida" :key="i" dense class="mb-5">
              <v-col cols="12" md="10">
                <p class="custom-label">{{ q.label }}</p>
                <v-select
                  v-model="form[q.key]"
                  :items="q.options"
                  item-text="text"
                  item-value="value"
                  placeholder="Seleccione una opción"
                  solo
                  background-color="#4a4444"
                  dark
                  hide-details
                  dense
                  :readonly="!bloqueoEdicion"
                ></v-select>
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
                <p class="custom-label">{{ ant.label }}</p>
                <v-select
                  v-model="form[ant.key]"
                  :items="itemsCompletos"
                  item-text="text"
                  item-value="value"
                  placeholder="Seleccione una opción"
                  solo
                  background-color="#4a4444"
                  dark
                  hide-details
                  dense
                  :readonly="!bloqueoEdicion"
                ></v-select>
              </v-col>
            </v-row>
            <v-divider class="grey darken-3 mb-6"></v-divider>
            <h3 class="white--text text-h5 mb-4 font-weight-light">
              Evaluación física
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
                  background-color="#4a4444"
                  dark
                  hide-details
                  dense
                  placeholder="0.00"
                  :readonly="!bloqueoEdicion"
                ></v-text-field>
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
                    background-color="#4a4444"
                    dark
                    hide-details
                    dense
                    placeholder="Valor"
                    :readonly="!bloqueoEdicion"
                  ></v-text-field>
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
      <v-row no-gutters justify="end">
        <template v-if="modoEdicion">
          <v-btn
            v-if="!bloqueoEdicion"
            color="#635b5b"
            class="white--text mr-4 custom-btn"
            @click="bloqueoEdicion = true"
            >MODIFICAR DATOS</v-btn
          >
          <v-btn
            v-else
            color="success"
            class="white--text mr-4 custom-btn"
            @click="guardarCambios"
            >GUARDAR CAMBIOS</v-btn
          >
        </template>
        <v-btn
          v-if="paso >= 3"
          outlined
          color="#a39a9a"
          class="mr-4 custom-btn"
          @click="predecir"
        >
          <v-icon left small>fas fa-chart-line</v-icon>
          PREDICCIÓN {{ paso === 3 ? "PRELIMINAR" : "FINAL" }}
        </v-btn>
        <v-btn
          color="#635b5b"
          class="white--text custom-btn px-10"
          @click="siguiente"
        >
          {{ paso === 4 ? "FINALIZAR" : "SIGUIENTE" }}
        </v-btn>
      </v-row>
    </v-sheet>
  </v-container>
</template>

<script>
import {
  OpcionesCompletas,
  OpcionesBinarias,
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
      paso: 1,
      bloqueoEdicion: !this.modoEdicion,
      form: {
        apellido: this.datosIniciales.apellido || "",
        nombre: this.datosIniciales.nombre || "",
        genero: this.datosIniciales.genero || null,
        dni: this.datosIniciales.dni || "",
        edad: this.datosIniciales.edad || null,
        diabetico: this.datosIniciales.diabetico || null,
        renales: this.datosIniciales.renales || null,
        alcohol: this.datosIniciales.alcohol || null,
        ejercicio: this.datosIniciales.ejercicio || null,
        fumador: this.datosIniciales.fumador || null,
        anhedonia: this.datosIniciales.anhedonia || null,
        ant_cardio: this.datosIniciales.ant_cardio || null,
        ant_diabetes: this.datosIniciales.ant_diabetes || null,
        ant_asma: this.datosIniciales.ant_asma || null,
        altura: this.datosIniciales.altura || null,
        peso: this.datosIniciales.peso || null,
        presion_sis: this.datosIniciales.presion_sis || null,
        presion_dis: this.datosIniciales.presion_dis || null,
        colesterol: this.datosIniciales.colesterol || null,
        hdl: this.datosIniciales.hdl || null,
        trigliceridos: this.datosIniciales.trigliceridos || null,
        creatinina: this.datosIniciales.creatinina || null,
        pcr: this.datosIniciales.pcr || null,
        hemoglobina: this.datosIniciales.hemoglobina || null,
        acido_urico: this.datosIniciales.acido_urico || null,
        potasio: this.datosIniciales.potasio || null,
      },
      // LISTAS ESTÁNDAR PARA SELECTORES
      itemsBinarios: [
        { text: "Sí", value: OpcionesBinarias.SI },
        { text: "No", value: OpcionesBinarias.NO },
      ],
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
      itemsAlcohol: [
        { text: "Nunca en el último año", value: OpcionesAlcohol.NUNCA },
        { text: "Todos los días", value: OpcionesAlcohol.DIARIAMENTE },
        { text: "Casi todos los días", value: OpcionesAlcohol.CASI_DIARIO },
        {
          text: "3 a 4 veces por semana",
          value: OpcionesAlcohol.TRES_CUATRO_SEMANA,
        },
        { text: "2 veces por semana", value: OpcionesAlcohol.DOS_VECES_SEMANA },
        { text: "Una vez por semana", value: OpcionesAlcohol.UNA_VEZ_SEMANA },
        { text: "2 a 3 veces por mes", value: OpcionesAlcohol.DOS_TRES_MES },
        { text: "Una vez al mes", value: OpcionesAlcohol.UNA_VEZ_MES },
        {
          text: "7 a 11 veces en el último año",
          value: OpcionesAlcohol.SIETE_ONCE_AÑO,
        },
        {
          text: "3 a 6 veces en el último año",
          value: OpcionesAlcohol.TRES_SEIS_AÑO,
        },
        {
          text: "1 a 2 veces en el último año",
          value: OpcionesAlcohol.UNA_DOS_AÑO,
        },
        { text: "No sabe / No recuerda", value: OpcionesAlcohol.NO_SABE },
      ],
      ItemsAnhedonia: [
        { text: "Para nada", value: OpcionesAnhedonia.NADA },
        { text: "Varios días", value: OpcionesAnhedonia.VARIOS_DIAS },
        {
          text: "Más de la mitad de los días",
          value: OpcionesAnhedonia.MAS_DE_LA_MITAD,
        },
        { text: "Casi todos los días", value: OpcionesAnhedonia.CASI_DIARIO },
        { text: "No sabe / No recuerda", value: OpcionesAnhedonia.NO_SABE },
      ],
      titulos: [
        "Datos personales",
        "Estilo de vida",
        "Antecedentes familiares",
        "Resultados de laboratorio",
      ],

      // CONFIGURACIÓN DE PREGUNTAS DINÁMICAS (PASO 2)
      preguntasVida: [],
      antecedentesFamiliaresConfig: [
        { key: "ant_cardio", label: "Enfermedad cardiovascular" },
        { key: "ant_diabetes", label: "Diabetes" },
        { key: "ant_asma", label: "Asma" },
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
          titulo: "Hematología y otros",
          campos: [
            { key: "hemoglobina", label: "Hemoglobina" },
            { key: "acido_urico", label: "Ácido úrico" },
            { key: "potasio", label: "Potasio" },
          ],
        },
      ],
    };
  },
  created() {
    // Definimos las preguntas de vida vinculándolas a sus opciones correspondientes
    this.preguntasVida = [
      {
        key: "alcohol",
        label: "Frecuencia de consumo de alcohol",
        options: this.itemsAlcohol,
      },
      {
        key: "ejercicio",
        label: "Días de actividad física moderada",
        options: [
          { text: "0 días", value: 0 },
          { text: "1 días", value: 1 },
          { text: "2 días", value: 2 },
          { text: "3 días", value: 3 },
          { text: "4 días", value: 4 },
          { text: "5 días", value: 5 },
          { text: "6 días", value: 6 },
          { text: "7 días", value: 7 },
        ],
      },
      {
        key: "fumador",
        label: "¿Ha fumado al menos 100 cigarrillos?",
        options: this.itemsCompletos,
      },
      {
        key: "anhedonia",
        label: "Presencia de Anhedonia",
        options: this.ItemsAnhedonia,
      },
    ];
  },
  methods: {
    siguiente() {
      if (this.paso < 4) this.paso++;
      else this.$emit("finalizar", this.form);
    },
    manejarAtras() {
      if (this.paso > 1) this.paso--;
      else this.$emit("atras");
    },
    async predecir() {
      console.log("Enviando a IA:", this.form);
      alert("Consultando modelo de predicción...");
    },
    guardarCambios() {
      this.bloqueoEdicion = false;
      this.$emit("guardar", this.form);
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
.v-text-field--solo >>> .v-input__control,
.v-select >>> .v-input__control {
  min-height: 40px !important;
  border-radius: 4px;
}
.custom-btn {
  height: 42px !important;
  font-size: 0.75rem;
  font-weight: bold;
}
</style>
