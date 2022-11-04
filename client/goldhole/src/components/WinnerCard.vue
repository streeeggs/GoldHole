<template>
  <v-card class="pa-6 rounded-sm mx-12 my-12">
    <v-card-title v-text="title" />
    <v-row align="center" class="mx-0">
      <div
        v-for="(user, i) in top"
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
          v-text="user"
        ></div>
      </div>
    </v-row>
    <v-row>
      <discovery-line :chartData="chartData" />
    </v-row>
  </v-card>
</template>

<script>
import DiscoveryLine from "../components/DiscoveryLine";
export default {
  name: "WinnerCard",
  components: {
    DiscoveryLine,
  },
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
  color: rgba(68, 68, 68, 0.4);
}

.bronze {
  color: rgba(78, 32, 13, 0.4);
}

.text-lottery {
  background: #222 -webkit-gradient(
      linear,
      left top,
      right top,
      from(#222),
      to(#222),
      color-stop(0.9, #fff)
    ) 0 0 no-repeat;
  animation: linear shine 3s infinite;
  background-size: 30%;
  background-clip: text;
  font-weight: bolder;
  text-shadow: 1px 1px #000000;
}

@keyframes shine {
  0% {
    background-position: 200%;
  }
  25% {
    background-position: top right;
  }
  50% {
    background-position: top;
  }
  75% {
    background-position: top left;
  }
  100% {
    background-position: -100%;
  }
}
</style>
