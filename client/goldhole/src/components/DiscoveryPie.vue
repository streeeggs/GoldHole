<template>
  <v-card class="pa-6 rounded-sm mx-12 my-12">
    <v-card-title v-text="title"></v-card-title>
    <v-card-text>
      <Doughnut
        v-if="loaded"
        :chart-options="chartOptions"
        :chart-data="chartData"
        :chart-id="chartId"
        :dataset-id-key="datasetIdKey"
        :width="width"
        :height="height"
      />
    </v-card-text>
  </v-card>
</template>

<script>
import { Doughnut } from "vue-chartjs/legacy";

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
} from "chart.js";

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);

export default {
  name: "DoughnutChart",
  components: {
    Doughnut,
  },
  props: {
    chartId: {
      type: String,
      default: "doughnut-chart",
    },
    datasetIdKey: {
      type: String,
      default: "label",
    },
    chartData: {
      default: () => {},
    },
    loaded: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
      default: "",
    },
    width: {
      type: Number,
      default: 400,
    },
    height: {
      type: Number,
      default: 400,
    },
  },
  data() {
    return {
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            labels: {
              color: "white",
            },
          },
        },
      },
    };
  },
};
</script>
