<template>
  <v-container
    fluid
    class="pa-0 d-flex align-center justify-center"
    style="min-height: calc(100vh - 64px - 36px); background-color: #121212"
  >
    <v-row no-gutters justify="center" align="center">
      <v-col cols="12" class="d-flex justify-center">
        <div class="logo-circle">
          <v-img
            :src="require('@/assets/images/logo-grande.png')"
            contain
            max-height="350"
            alt="CardioPredict Logo"
          ></v-img>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "IndexPage",
};
</script>

<style scoped>
.logo-circle {
  background-color: white;
  width: 500px;
  height: 500px;
  border-radius: 50%;
  /* Flexbox interno para centrar la imagen dentro del círculo */
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 50px;
  border: 6px solid #26c6da;
  box-shadow: 0px 15px 35px rgba(0, 0, 0, 0.6);
}

/* Responsividad para pantallas pequeñas */
@media (max-height: 750px) {
  .logo-circle {
    width: 380px;
    height: 380px;
    padding: 40px;
  }
}

@media (max-width: 600px) {
  .logo-circle {
    width: 280px;
    height: 280px;
    padding: 30px;
  }
}
</style>
