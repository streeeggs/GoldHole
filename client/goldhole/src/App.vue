<template>
  <v-app>
    <v-main>
      <router-view />
      <v-snackbar v-model="snackbar">
        {{ text }}
        <template v-slot:action="{ attrs }">
          <v-btn color="gold" text v-bind="attrs" @click="snackbar = false">
            Close
          </v-btn>
        </template>
      </v-snackbar>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "GoldHole",
  data: () => ({
    snackbar: true,
    text: `Goldhole won't be updated between 2/4-2/11. Don't say anything worth recording until then.`,
  }),
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
