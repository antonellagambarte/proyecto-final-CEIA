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
        @click="atras"
        style="width: fit-content"
      >
        <v-icon small color="grey lighten-1">fas fa-arrow-left</v-icon>
        <span class="grey--text text--lighten-1 caption ml-2"
          >Nuevo paciente</span
        >
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
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row dense class="mb-6">
              <v-col cols="12" md="4">
                <p class="custom-label">Género</p>
                <v-select
                  :items="['Masculino', 'Femenino']"
                  solo
                  background-color="#4a4444"
                  dark
                  hide-details
                  dense
                ></v-select>
              </v-col>
              <v-col cols="12" md="3" offset-md="1">
                <p class="custom-label">DNI</p>
                <v-text-field
                  solo
                  background-color="#4a4444"
                  dark
                  hide-details
                  dense
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="2" offset-md="1">
                <p class="custom-label">Edad</p>
                <v-text-field
                  solo
                  background-color="#4a4444"
                  dark
                  hide-details
                  dense
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
                  :items="['Sí', 'No']"
                  solo
                  background-color="#4a4444"
                  dark
                  hide-details
                  dense
                ></v-select>
              </v-col>
              <v-col cols="12" md="5" offset-md="1" class="mb-3">
                <p class="custom-label">¿Tiene problemas renales?</p>
                <v-select
                  :items="['Sí', 'No']"
                  solo
                  background-color="#4a4444"
                  dark
                  hide-details
                  dense
                ></v-select>
              </v-col>
            </v-row>
          </div>

          <div v-if="paso === 2">
            <v-row v-for="(q, i) in preguntasVida" :key="i" dense class="mb-5">
              <v-col cols="12" md="10">
                <p class="custom-label">{{ q.label }}</p>
                <v-select
                  :items="q.options"
                  solo
                  background-color="#4a4444"
                  dark
                  hide-details
                  dense
                ></v-select>
              </v-col>
            </v-row>
          </div>

          <div v-if="paso === 3">
            <v-row dense class="mb-4">
              <v-col
                cols="12"
                md="5"
                v-for="ant in ['Enfermedad cardiovascular', 'Diabetes', 'Asma']"
                :key="ant"
                class="mb-4"
              >
                <p class="custom-label">{{ ant }}</p>
                <v-select
                  :items="['Sí', 'No']"
                  solo
                  background-color="#4a4444"
                  dark
                  hide-details
                  dense
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
                v-for="itemF in [
                  'Altura (m)',
                  'Peso (Kg)',
                  'Presión sistólica',
                  'Presión distólica',
                ]"
                :key="itemF"
              >
                <p class="custom-label">{{ itemF }}</p>
                <v-text-field
                  solo
                  background-color="#4a4444"
                  dark
                  hide-details
                  dense
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
                  :key="campo"
                  cols="12"
                  md="4"
                >
                  <p class="custom-label">{{ campo }}</p>
                  <v-text-field
                    solo
                    background-color="#4a4444"
                    dark
                    hide-details
                    dense
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
        <v-btn
          v-if="paso >= 3"
          outlined
          color="#a39a9a"
          class="mr-4 custom-btn"
          @click="predecir"
        >
          <v-icon left small>fas fa-chart-line</v-icon>
          REALIZAR PREDICCIÓN {{ paso === 3 ? "PRELIMINAR" : "FINAL" }}
        </v-btn>
        <v-btn
          v-if="paso >= 3"
          color="#635b5b"
          class="white--text mr-4 custom-btn"
          @click="guardar"
          >GUARDAR DATOS</v-btn
        >
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
  background-color: #635b5b !important; /* Color gris de los botones */
}
</style>

<script>
export default {
  data() {
    return {
      paso: 1,
      titulos: [
        "Datos personales",
        "Estilo de vida",
        "Antecedentes familiares",
        "Resultados de laboratorio",
      ],
      form: { apellido: "", nombre: "" },
      preguntasVida: [
        {
          label: "Frecuencia de consumo de alcohol",
          options: ["Nunca", "Ocasionalmente", "Semanal", "Diario"],
        },
        {
          label: "Días de actividad física moderada",
          options: ["0 días", "1-2 días", "3-5 días", "+5 días"],
        },
        {
          label: "¿Ha fumado al menos 100 cigarrillos?",
          options: ["Sí", "No"],
        },
        { label: "Presencia de Anhedonia", options: ["Sí", "No"] },
      ],
      laboratorio: [
        {
          titulo: "Perfil lipídico",
          campos: ["Colesterol total", "HDL", "Triglicéridos"],
        },
        { titulo: "Función renal", campos: ["Creatinina", "Proteína C (PCR)"] },
        {
          titulo: "Hematología y otros",
          campos: ["Hemoglobina", "Ácido úrico", "Potasio"],
        },
      ],
    };
  },
  methods: {
    siguiente() {
      if (this.paso < 4) this.paso++;
    },
    atras() {
      if (this.paso > 1) this.paso--;
      else this.$router.push("/");
    },
    guardar() {
      alert("Datos guardados");
    },
    predecir() {
      alert("Calculando...");
    },
  },
};
</script>
