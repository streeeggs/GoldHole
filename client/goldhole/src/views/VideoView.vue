<template>
  <div>
    <nav-template />
    <winner-card :top="videosTopData.labels" />
    <top-chart
      :chart-data="videosData"
      :loaded="loaded"
      chart-id="topVideos"
      title="Ranking of Topics"
    />
    <discovery-line
      :chart-data="videoHistoryData"
      :loaded="historyLoaded"
      :items="videosTopData.labels"
      title="History of Discovery"
    />
    <discovery-pie
      :chart-data="videosTopData"
      :loaded="topLoaded"
      title="Most Echoes"
    />
  </div>
</template>

<script>
import VideoService from "../service/VideoService";
import { coulmnToDataset } from "../components/dataMappingUtil";

import NavTemplate from "../components/NavTemplate";
import TopChart from "../components/TopChart";
import DiscoveryPie from "../components/DiscoveryPie";
import DiscoveryLine from "../components/DiscoveryLine";
import WinnerCard from "../components/WinnerCard";
import { videoHistorySelection } from "../store/store";

export default {
  name: "VideosView",
  components: {
    NavTemplate,
    DiscoveryPie,
    DiscoveryLine,
    WinnerCard,
    TopChart,
  },
  videoService: null,
  watch: {
    "videoHistorySelection.item": {
      handler(val) {
        this.getHistoryData(val);
      },
      deep: true,
    },
  },
  created() {
    this.videoService = new VideoService();
  },
  methods: {
    getTopData() {
      this.topLoaded = false;
      try {
        this.videoService.getTopVideos().then((data) => {
          this.videosTopData = coulmnToDataset(
            data.slice(0, 20),
            "Title",
            "Count",
            true,
            true
          );
        });
        this.topLoaded = true;
      } catch (e) {
        console.error(e);
      }
    },
    getHistoryData(title) {
      this.historyLoaded = false;
      this.videoService.getHistory(title).then((data) => {
        this.videoHistoryData.labels = data.map((d) => d._id.date);
        this.videoHistoryData.datasets[0].data = data.map((d) => d.Count);
        this.videoHistoryData.datasets[0].label = title;
      });
      this.historyLoaded = true;
    },
    getTotalData() {
      this.loaded = false;
      this.videoService.getTopVideos().then((data) => {
        this.videosData = coulmnToDataset(data.slice(0, 20), "Title", "Count");
        this.videosData.datasets[0].label =
          "A collective of efforts quantified";
        this.videosData.datasets[0].backgroundColor = [
          "rgba(91, 192, 222, 0.4)",
        ];
        this.videosData.datasets[0].borderColor = ["rgba(91, 192, 222, 1)"];
      });
      this.loaded = true;
    },
  },
  async mounted() {
    this.getTopData();
    this.getHistoryData(this.videoHistorySelection.item);
    this.getTotalData();
  },
  data() {
    return {
      loaded: false,
      topLoaded: false,
      historyLoaded: false,
      videosData: {
        labels: [],
        datasets: [
          { data: [], label: "", backgroundColor: [], borderColor: [] },
        ],
      },
      videosTopData: {
        labels: [""],
        datasets: [
          {
            data: [],
          },
        ],
      },
      videoHistoryData: {
        labels: [],
        datasets: [
          { label: "", data: [], borderColor: "rgba(205, 175, 20, 0.4)" },
        ],
      },
      videoHistorySelection,
    };
  },
};
</script>
