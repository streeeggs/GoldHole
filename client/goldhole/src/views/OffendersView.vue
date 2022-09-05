<template>
  <div>
    <nav-template />
    <winner-card
      :top="Object.keys(topData.datasets[0].data)"
      title="Number 1 Offender"
    />
    <top-chart
      :chart-data="topData"
      :loaded="topLoaded"
      chart-id="topOffenders"
      title="Ranking Offenders"
    />
    <user-table
      title="Recorded Evidence"
      :data="offenderData"
      :loaded="offenderLoaded"
    />
    <radar-chart
      :title="
        'Anatomy of ' +
        Object.keys(topData.datasets[0].data)[0] +
        '\'s Contributions'
      "
      chart-id="anatomyofacriminal"
      :chartData="hisData"
    />
  </div>
</template>

<script>
import UserService from "../service/UserService";

import {
  objectToDataset,
  coulmnToDataset,
} from "../components/dataMappingUtil";
import TopChart from "../components/TopChart";
import UserTable from "../components/UserTable";
import NavTemplate from "../components/NavTemplate";
import WinnerCard from "../components/WinnerCard";
import RadarChart from "../components/RadarChart";

export default {
  name: "OffendersView",

  components: {
    UserTable,
    TopChart,
    NavTemplate,
    WinnerCard,
    RadarChart,
  },
  userService: null,
  watch: {
    options: {
      handler() {
        this.getTopOffenderMessagesFromApi();
        this.getOffenderDataFromApi();
        this.getMessagesFromTopOffenderFromApi();
      },
      deep: true,
    },
  },
  async mounted() {
    this.getTopOffenderMessagesFromApi();
    this.getOffenderDataFromApi();
    this.getMessagesFromTopOffenderFromApi();
  },
  methods: {
    getOffenderDataFromApi() {
      this.offenderLoaded = false;
      try {
        this.userService.getUsers().then((data) => {
          this.offenderData = data;
        });
        this.offenderLoaded = true;
      } catch (e) {
        console.log(e);
      }
    },
    getTopOffenderMessagesFromApi() {
      this.topLoaded = false;
      try {
        this.userService.getTopOffendersByMessage().then((data) => {
          this.topData = objectToDataset(data["Count"]);
          this.topData.datasets[0].backgroundColor = [
            "rgba(205, 175, 20, 0.4)",
          ];
          this.topData.datasets[0].label = "A culmination of effort quantified";
        });
        this.topLoaded = true;
      } catch (e) {
        console.error(e);
      }
    },
    getMessagesFromTopOffenderFromApi() {
      this.hesLoaded = false;
      try {
        this.userService.getTopOffenderAndMessages().then((data) => {
          this.hisData = coulmnToDataset(
            data.slice(0, 10).sort(() => {
              return 0.5 - Math.random();
            }),
            "Message",
            "Count",
            false,
            true
          );
          this.hisData.datasets[0].backgroundColor = [
            "rgba(205, 175, 20, 0.4)",
          ];
          this.hisData.datasets[0].label = "His influence is palpable";
          this.hisData.datasets[0].pointHoverBackgroundColor = "white";
          this.hisData.datasets[0].pointHoverBorderColor = "white";
        });
        this.hesLoaded = true;
      } catch (e) {
        console.error(e);
      }
    },
  },
  created() {
    this.userService = new UserService();
  },
  data() {
    return {
      topData: {
        datasets: [
          {
            data: [],
            label: "",
            backgroundColor: [],
            borderColor: [],
            borderWidth: 1,
          },
        ],
      },
      hisData: {
        datasets: [
          {
            data: [],
            label: "",
            backgroundColor: [],
            borderColor: [],
            borderWidth: 1,
          },
        ],
      },
      hesLoaded: false,
      topLoaded: false,
      offenderLoaded: false,
      offenderData: [{}],
    };
  },
};
</script>
