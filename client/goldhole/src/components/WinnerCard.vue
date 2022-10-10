<template>
  <v-card class="pa-6 rounded-sm mx-12 my-12">
    <v-card-title v-text="title" />
    <div class="text-h1 text-center lottery" v-text="top[0]"></div>
  </v-card>
</template>

<script>
export default {
  name: "WinnerCard",
  props: {
    top: {
      type: Array,
      default: () => ["Soon"],
    },
    chartData: {
      type: Object,
      default: () => {},
    },
    title: {
      type: String,
      default: "Nothing here yet",
    },
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
