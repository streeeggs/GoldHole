<template>
  <div>
    <v-navigation-drawer v-model="drawer" temporary app>
      <v-list nav dense>
        <v-list-item-group v-model="selectedItem" color="primary">
          <v-list-item v-for="(item, i) in items" :key="i" :to="item.url">
            <v-list-item-icon>
              <v-icon v-text="item.icon"></v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title v-text="item.title"> </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar elevate-on-scroll>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-spacer />
      <v-toolbar-title>
        <v-btn text x-large :to="items[0].url">
          <v-img
            :src="require('../assets/logo_sm.png')"
            max-height="45"
            contain
          />
        </v-btn>
      </v-toolbar-title>
      <v-spacer />
    </v-app-bar>
  </div>
</template>

<script>
export default {
  name: "NavTemplate",

  data() {
    return {
      selectedItem: 1,
      drawer: false,
      items: [
        { title: "Home", icon: "mdi-home", url: "/" },
        { title: "Offenders", icon: "mdi-human-queue", url: "/offenders" },
        { title: "Videos", icon: "mdi-youtube", url: "/videos" },
      ],
      right: null,
    };
  },
};
</script>
