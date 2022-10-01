<template>
  <div>
    <nav-template />
    <winner-card :top="['idk soemthing']" title="Gold that defines us" />
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
