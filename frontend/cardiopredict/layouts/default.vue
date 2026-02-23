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

      <v-list nav class="mt-2">
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
          class="my-2 custom-item"
        >
          <v-list-item-action>
            <v-icon size="20" class="item-icon">{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title class="item-text" v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar fixed app flat color="#1e1e1e" />

    <v-main style="background-color: #121212; height: 100vh; overflow: hidden">
      <v-container fluid class="pa-0">
        <Nuxt />
      </v-container>
    </v-main>

    <v-footer app flat color="#1e1e1e" class="justify-center">
      <span class="grey--text text--darken-1 caption">
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
      items: [
        {
          icon: "fas fa-home",
          title: "Inicio",
          to: "/",
        },
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

/* Estilo de los items (texto e icono blancos por defecto) */
.item-text,
.item-icon {
  color: #ffffff !important;
}

/* Color cian solo para el ítem activo, tal como estaba antes */
.v-list-item--active .item-text,
.v-list-item--active .item-icon {
  color: #26c6da !important;
}

/* Fondo gris oscuro para el ítem activo para que se parezca a tu imagen 1 */
.v-list-item--active {
  background-color: #4a4444 !important;
}
</style>
