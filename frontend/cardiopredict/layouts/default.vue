<template>
  <v-app dark>
    <v-navigation-drawer v-model="drawer" fixed app color="#2c2525" width="260">
      <div class="logo-sidebar-header">
        <v-img
          :src="require('@/assets/images/image-cardio.png')"
          contain
          height="50"
          position="left center"
          class="ml-4"
        ></v-img>
      </div>

      <v-divider></v-divider>

      <v-list nav>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
          class="my-2"
        >
          <v-list-item-action>
            <v-icon size="20" color="white">{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title class="white--text" v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar fixed app flat color="#1e1e1e">
      <v-btn icon>
        <v-icon>fas fa-bell</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>fas fa-user-circle</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main style="background-color: #121212; height: 100vh; overflow: hidden">
      <v-container fluid class="pa-0">
        <Nuxt />
      </v-container>
    </v-main>

    <v-footer app flat color="#1e1e1e" class="justify-center">
      <span class="grey--text text--darken-1">
        &copy; {{ new Date().getFullYear() }} - CardioPredict AI
      </span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      drawer: true,
      // ESTA ES LA LISTA QUE FALTABA:
      items: [
        {
          icon: "fas fa-user-plus",
          title: "Nuevo paciente",
          to: "/nuevo-paciente",
        },
        {
          icon: "fas fa-history",
          title: "Historial",
          to: "/historial",
        },
        {
          icon: "fas fa-chart-line",
          title: "Análisis",
          to: "/analisis",
        },
      ],
    };
  },
};
</script>

<style scoped>
.logo-sidebar-header {
  background-color: white;
  height: 64px;
  display: flex;
  align-items: center;
}

/* Color cian para el ítem activo */
.v-list-item--active .v-list-item__title,
.v-list-item--active .v-icon {
  color: #26c6da !important;
}
</style>
