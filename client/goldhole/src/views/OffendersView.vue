<template>
  <div>
    <nav-template />
    <winner-card
      :top="topOffendersList"
      :chartData="topOffendersDetail"
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
      :data="messageData"
      :loaded="messagesLoaded"
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
import MessageService from "../service/MessageService";

import TopChart from "../components/TopChart";
import UserTable from "../components/UserTable";
import NavTemplate from "../components/NavTemplate";
import WinnerCard from "../components/WinnerCard";
// Kill for now
//import RadarChart from "../components/RadarChart";
import { userDateBins } from "../store/store";
import { coulmnToDataset } from "../components/dataMappingUtil";

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
  messageService: null,
  watch: {
    "userDateBins.item": {
      handler(val) {
        this.getTopOffenderByDateRange(val);
      },
      deep: true,
    },
  },
  async mounted() {
    this.getTopOffenderMessagesFromApi(this.userDateBins.item);
    this.getMessages();
    this.getTopOffenderByDateRange(this.userDateBins.item);
  },
  methods: {
    getMessages() {
      this.messagesLoaded = false;
      try {
        this.messageService.getMessages().then((data) => {
          this.messageData = data;
        });
        this.messagesLoaded = true;
      } catch (e) {
        console.log(e);
      }
    },
    getTopOffenderMessagesFromApi(dateRange) {
      this.topLoaded = false;
      try {
        this.userService.getOffenderCount(dateRange).then((data) => {
          data = data.slice(0, 30);
          this.topData = coulmnToDataset(data, "user", "totalFavor");
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
    getTopOffenderByDateRange(dateRange) {
      this.historyLoaded = false;
      this.userService.getTopOffenderBinned(dateRange).then((data) => {
        this.topOffendersDetail = data[0].perdate;
        this.topOffendersList = data[0].totals.map((rec) => rec.name);
      });
      this.historyLoaded = true;
    },
  },
  created() {
    this.userService = new UserService();
    this.messageService = new MessageService();
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
      messagesLoaded: false,
      historyLoaded: false,
      dataLoaded: false,
      messageData: [{}],
      topOffendersList: [],
      topOffendersDetail: {
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
