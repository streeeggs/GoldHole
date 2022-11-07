<template>
  <v-card
    class="pa-6 rounded-sm mx-12 my-12"
    v-if="
      chartData.datasets.some((d) =>
        d.data.some((obj) => Object.getOwnPropertyNames(obj).length > 0)
      )
    "
  >
    <v-card-title v-text="title" />
    <v-select
      v-if="items"
      v-model="videoHistorySelection.item"
      :items="items"
      label="Look for others idk"
    />
    <LineChartGenerator
      :chart-id="chartId"
      :chart-options="chartOptions"
      :chart-data="chartData"
    />
  </v-card>
</template>

<script>
import { videoHistorySelection } from "../store/store";

import { Line as LineChartGenerator } from "vue-chartjs/legacy";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  TimeScale,
  PointElement,
} from "chart.js";
import "chartjs-adapter-moment";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  TimeScale,
  PointElement
);

export default {
  name: "LineChart",
  components: {
    LineChartGenerator,
  },
  props: {
    chartOptions: {
      type: Object,
      default: () => ({
        responsive: true,
        maintainAspectRatio: false,
      }),
    },
    chartData: {
      type: Object,
      required: true,
    },
    chartId: {
      type: String,
      default: "discovery-line",
    },
    title: {
      type: String,
      default: "",
    },
    items: {
      type: Array,
    },
  },
  data() {
    return {
      videoHistorySelection,
    };
  },
};
</script>
