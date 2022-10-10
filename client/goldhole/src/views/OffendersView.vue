<template>
  <div>
    <nav-template />
    <winner-card
      :top="topOffenderData"
      :charData="topOffenderHistory"
      title="Your Winners"
    />
    <top-chart
      :chart-data="topData"
      :loaded="topLoaded"
      chart-id="topOffenders"
      title="Total Ranking"
    />
    <user-table
      title="Recorded Wins"
      :data="offenderData"
      :loaded="offenderLoaded"
    />
    <!-- kill for now 
    <radar-chart
      :title="
        'Anatomy of ' +
        Object.keys(topData.datasets[0].data)[0] +
        '\'s Contributions'
      "
      chart-id="anatomyofacriminal"
      :chartData="hisData"
    /> -->
  </div>
</template>

<script>
import UserService from "../service/UserService";

import {
  objectToDataset,
  // Kill for now
  //coulmnToDataset,
  mapUserDataResultToLine,
} from "../components/dataMappingUtil";
import TopChart from "../components/TopChart";
import UserTable from "../components/UserTable";
import NavTemplate from "../components/NavTemplate";
import WinnerCard from "../components/WinnerCard";
// Kill for now
//import RadarChart from "../components/RadarChart";
import { userDateBins } from "../store/store";

export default {
  name: "OffendersView",

  components: {
    UserTable,
    TopChart,
    NavTemplate,
    WinnerCard,
    //Kill for now
    //RadarChart,
  },
  userService: null,
  watch: {
    "userDateBins.item": {
      handler(val) {
        this.getTopOffenderByDateRange(val);
      },
      deep: true,
    },
  },
  async mounted() {
    this.getTopOffenderMessagesFromApi();
    this.getOffenderDataFromApi();
    //this.getMessagesFromTopOffenderFromApi();
    this.getTopOffenderByDateRange(this.userDateBins.item);
    this.getTopOffenders(this.userDateBins.item);
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
    // Kill for now
    // getMessagesFromTopOffenderFromApi() {
    //   this.hesLoaded = false;
    //   try {
    //     this.userService.getTopOffenderAndMessages().then((data) => {
    //       this.hisData = coulmnToDataset(
    //         data.slice(0, 10).sort(() => {
    //           return 0.5 - Math.random();
    //         }),
    //         "Message",
    //         "Count",
    //         false,
    //         true
    //       );
    //       this.hisData.datasets[0].backgroundColor = [
    //         "rgba(205, 175, 20, 0.4)",
    //       ];
    //       this.hisData.datasets[0].label = "His influence is palpable";
    //       this.hisData.datasets[0].pointHoverBackgroundColor = "white";
    //       this.hisData.datasets[0].pointHoverBorderColor = "white";
    //     });
    //     this.hesLoaded = true;
    //   } catch (e) {
    //     console.error(e);
    //   }
    // },
    getTopOffenderByDateRange(dateRange) {
      this.historyLoaded = false;
      this.userService.getTopOffenderBinned(dateRange).then((data) => {
        this.topOffenderHistory = mapUserDataResultToLine(data);
      });
      this.historyLoaded = true;
    },
    getTopOffenders(dateRange) {
      // TODO: Properly load w/ own varible
      this.dataLoaded = false;
      this.userService.getTopOffenders(dateRange).then((data) => {
        this.topOffenderData = data.map((rec) => rec.name);
      });
      this.dataLoaded = true;
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
      topLoaded: false,
      offenderLoaded: false,
      historyLoaded: false,
      dataLoaded: false,
      offenderData: [{}],
      topOffenderData: [],
      topOffenderHistory: {
        labels: [],
        datasets: [
          { label: "", data: [], borderColor: "rgba(205, 175, 20, 0.4)" },
        ],
      },
      userDateBins,
    };
  },
};
</script>
