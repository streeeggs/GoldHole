<template>
  <v-card class="pa-6 rounded-sm mx-12 my-12">
    <v-card-title v-text="title" />
    <v-select v-model="userDateBins.item" :items="items" label="Date Range" />
    <LineChartGenerator :chart-options="chartOptions" :chart-data="chartData" />
  </v-card>
</template>

<script>
// TODO: Make this a prop so I can reduce the two line chart components
import { userDateBins } from "../store/store";

import { Line as LineChartGenerator } from "vue-chartjs/legacy";

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  CategoryScale,
  PointElement,
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  CategoryScale,
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
    title: {
      type: String,
      default: "",
    },
    items: {
      default: () => [],
    },
  },
  data() {
    return {
      userDateBins,
    };
  },
};
</script>
