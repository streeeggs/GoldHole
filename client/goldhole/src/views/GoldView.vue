<template>
  <div>
    <nav-template />
    <winner-card :top="['Soon']" title="One day, this will make you rich" />
  </div>
</template>

<script>
import NavTemplate from "../components/NavTemplate";
import WinnerCard from "../components/WinnerCard";

export default {
  name: "GoldView",
  components: {
    NavTemplate,
    WinnerCard,
  },
};
</script>
