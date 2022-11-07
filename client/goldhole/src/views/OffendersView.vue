<template>
  <div>
    <nav-template />
    <v-card
      class="pa-2 rounded-sm mx-auto sticky-card float-right"
      maxWidth="500"
    >
      <v-select
        v-model="userDateBins.item"
        :items="dateBins"
        label="Show by..."
      />
    </v-card>
    <winner-card :top="topOffendersList" title="Those to be followed" />
    <discovery-line
      :chartData="topOffendersDetail"
      :chartOptions="byDateChartOptions"
      title="By Date"
      chart-id="ByDate"
    />
    <top-chart
      :chartData="topData"
      :loaded="topLoaded"
      chart-id="topOffenders"
      title="Where do the rest stand?"
    />
    <user-table
      title="Recorded Evidence"
      :data="messageData"
      :loaded="messagesLoaded"
    />
  </div>
</template>

<script>
import UserService from "../service/UserService";
import MessageService from "../service/MessageService";

import TopChart from "../components/TopChart";
import UserTable from "../components/UserTable";
import NavTemplate from "../components/NavTemplate";
import WinnerCard from "../components/WinnerCard";
import { userDateBins } from "../store/store";
import {
  mapTopUserDataResultToBar,
  mapUserDataResultToLine,
} from "../components/dataMappingUtil";
import DiscoveryLine from "../components/DiscoveryLine.vue";
import { DATE_BINS, mapDateBinToTimescaleUnit } from "../components/enums";

export default {
  name: "OffendersView",

  components: {
    UserTable,
    TopChart,
    NavTemplate,
    WinnerCard,
    DiscoveryLine,
  },
  watch: {
    "userDateBins.item": {
      handler(val) {
        this.getTopOffenderByDateRange(val);
        this.getTopOffenderMessagesFromApi(val);
        this.getMessages();
      },
      immediate: true,
    },
  },
  computed: {
    // TODO: Move into line chart component
    byDateChartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            type: "time",
            time: {
              unit: mapDateBinToTimescaleUnit(this.userDateBins.item),
            },
            grid: {
              color: "rgba(255, 255, 255, 0)",
              borderColor: "rgba(255, 255, 255, 0)",
              tickColor: "white",
            },
            ticks: {
              color: "white",
            },
          },
          y: {
            grid: {
              color: "rgba(255, 255, 255, 0.2)",
              tickColor: "white",
            },
            ticks: {
              color: "white",
            },
          },
        },
        plugins: {
          legend: {
            labels: {
              color: "white",
            },
          },
        },
      };
    },
  },
  methods: {
    async getMessages() {
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
    async getTopOffenderMessagesFromApi(dateRange) {
      this.topLoaded = false;
      try {
        this.userService.getOffenderCount(dateRange).then((data) => {
          this.topData = mapTopUserDataResultToBar(data, [
            "A culmination of efforts quantified",
          ]);
        });
        this.topLoaded = true;
      } catch (e) {
        console.error(e);
      }
    },
    async getTopOffenderByDateRange(dateRange) {
      this.historyLoaded = false;
      this.userService.getTopOffenderBinned(dateRange).then((data) => {
        this.topOffendersList = data[0].totals.map((rec) => rec.name);
        this.topOffendersDetail = mapUserDataResultToLine(
          data[0].perdate,
          true
        );
      });
      this.historyLoaded = true;
    },
  },
  data() {
    return {
      topData: {
        labels: [],
        datasets: [
          { label: "", data: [], borderColor: "rgba(205, 175, 20, 0.4)" },
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
      dateBins: DATE_BINS,
      userService: new UserService(),
      messageService: new MessageService(),
    };
  },
};
</script>
<style scoped>
.sticky-card {
  position: sticky;
  top: 50px;
  z-index: 10;
}
</style>
