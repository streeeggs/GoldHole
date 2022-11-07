<template>
  <v-card class="pa-6 rounded-sm mx-12 my-12">
    <v-card-title v-text="title" />
    <v-row align="center" justify="center" class="mx-0" v-if="top.length > 0">
      <div
        v-for="(val, i) in top"
        :key="i"
        :class="rank[i]"
        class="d-flex justify-center align-center mb-6 pl-5 pr-5 pb-10"
      >
        <v-img
          :src="require(`../assets/${rank[i]}-bar.gif`)"
          :max-height="100 - i * 20"
          :max-width="100 - i * 20"
          class="flex-grow-0"
          contain
        />
        <div
          :class="'text-h' + (i + 1)"
          class="text-center text-lottery"
          v-text="val"
        ></div>
      </div>
    </v-row>
    <v-row v-else align="center" justify="center">
      <div class="text-center text-h2">Mail-in votes are still ariving...</div>
    </v-row>
  </v-card>
</template>

<script>
export default {
  name: "WinnerCard",
  components: {},
  props: {
    top: {
      type: Array,
      default: () => ["Soon", "You'll", "See"],
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
  data: function () {
    return {
      rank: ["gold", "silver", "bronze"],
    };
  },
};
</script>

<style scoped>
/*
  TODO: GET THIS IN THE ROOT CSS ALREADY
*/
.gold {
  color: rgba(205, 175, 20, 0.4);
}

.silver {
  color: rgba(68, 68, 68, 0.6);
}

.bronze {
  color: rgba(78, 32, 13, 0.6);
}

.text-lottery {
  background: linear-gradient(90deg, black, white, black);
  background-repeat: no-repeat;
  background-size: 80%;
  animation: shine 7s linear infinite;

  --webkit-background-clip: text;
  --webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: bolder;
  text-shadow: 1px 1px #000000;
}

@keyframes shine {
  from {
    background-position: 1000%;
  }
  to {
    background-position: -1000%;
  }
}
</style>
