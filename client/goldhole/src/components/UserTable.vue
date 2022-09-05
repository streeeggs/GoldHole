<template>
  <v-card class="pa-6 rounded-sm mx-12 my-12">
    <v-card-title>
      <v-col col="2">{{ title }}</v-col>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        class="shrink"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="data"
      :search="search"
    ></v-data-table>
  </v-card>
</template>

<script>
export default {
  name: "UserTable",
  props: {
    title: {
      type: String,
      default: "",
    },
    data: {
      default: () => [{}],
    },
    loaded: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      search: "",
      users: [],
      headers: [
        { text: "Favor", value: "Count" },
        {
          text: "Suspect",
          align: "start",
          sortable: true,
          value: "Name",
        },
        {
          text: "Offense",
          value: "Message",
        },
        { text: "Action Recorded", value: "Date" },
        { text: "Topic", value: "Title" },
      ],
    };
  },
};
</script>
