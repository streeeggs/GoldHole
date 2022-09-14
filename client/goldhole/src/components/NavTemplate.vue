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
      <template v-slot:append>
        <div class="d-flex flex-column align-center flex-wrap pa-2">
          <v-btn
            block
            tile
            text
            icon
            color="blue"
            href="https://github.com/streeeggs/GoldHole"
          >
            <span>Github</span>
            <v-icon>mdi-github</v-icon>
          </v-btn>
          <v-btn
            block
            tile
            text
            icon
            color="blue"
            href="mailto:forgotmycockli@protonmail.com?subject=Your%20shit%20sucks&body=Can%20you%20add%20sick%20tits%20and%20maybe%20make%20me%20the%20number%20one?%20K%20thanks"
          >
            <span>Mail</span>
            <v-icon>mdi-bomb</v-icon>
            <v-icon>mdi-mailbox-open-outline</v-icon>
          </v-btn>
          <span> Made by: <span class="lottery">streeeggs</span> </span>
          <span> With Help From: <span>Miles_Gloriosus</span> </span>
        </div>
      </template>
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

<style scoped>
.lottery {
  background: #222 -webkit-gradient(
      linear,
      left top,
      right top,
      from(#222),
      to(#222),
      color-stop(0.9, #fff)
    ) 0 0 no-repeat;
  animation: shine 4s infinite;
  background-size: 150px;
  color: rgba(205, 175, 20, 0.4);
  background-clip: text;
  font-weight: bolder;
  text-shadow: 1px 1px #000000;
}

@keyframes shine {
  0%,
  10% {
    background-position: -500px;
  }
  20% {
    background-position: top left;
  }
  90% {
    background-position: top right;
  }
  100% {
    background-position: 500px;
  }
}
</style>
