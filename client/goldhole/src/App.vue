<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "GoldHole",
  // methods: {
  //   chooseBackground() {
  //     this.background =
  //       this.backgroundUrls[
  //         Math.floor(Math.random() * this.backgroundUrls.length)
  //       ];
  //   },
  // },
  // mounted() {
  //   this.chooseBackground();
  // },
  // data() {
  //   return {
  //     backgroundUrls: [
  //       "https://media.giphy.com/media/RAmtrPUSxWvlwgszTU/giphy.gif",
  //       "https://media.giphy.com/media/26u6bQMgjKm4gyfwk/giphy.gif",
  //       "https://media.giphy.com/media/l41JQdHhPZ6NlegJq/giphy.gif",
  //       "https://media.giphy.com/media/T5tnw3xsSagXhUrSKD/giphy.gif",
  //     ],
  //     background: "https://media.giphy.com/media/RAmtrPUSxWvlwgszTU/giphy.gif",
  //   };
  // },
};
</script>
<style>
#app {
  background: repeat top/50rem #080808 url("./assets/main_bg.gif");
}
</style>
