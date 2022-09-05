<template>
  <v-card class="pa-6 rounded-sm mx-12 my-12">
    <v-card-title v-text="title" />
    <Radar
      :chart-options="chartOptions"
      :chart-data="chartData"
      :chart-id="chartId"
      :dataset-id-key="datasetIdKey"
      :width="width"
      :height="height"
    />
  </v-card>
</template>

<script>
import { Radar } from "vue-chartjs/legacy";
// FIXME: Not tree shakeable?
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

export default {
  name: "RadarChart",
  components: { Radar },
  props: {
    chartId: {
      type: String,
      default: "radar-chart",
    },
    chartData: {
      default: () => {},
    },
    datasetIdKey: {
      type: String,
      default: "label",
    },
    width: {
      type: Number,
      default: 400,
    },
    height: {
      type: Number,
      default: 400,
    },
    title: {
      type: String,
      default: "Anatomy of a criminal",
    },
    loaded: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          r: {
            grid: {
              color: "white",
            },
            pointLabels: {
              color: "white",
            },
            ticks: {
              display: false,
            },
          },
        },
        plugins: {
          legend: {
            display: false,
          },
        },
      },
    };
  },
};
</script>
