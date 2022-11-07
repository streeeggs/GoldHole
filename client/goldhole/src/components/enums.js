export const DATE_BINS = [
  {
    text: "Week",
    value: "WEEK",
  },
  {
    text: "Month",
    value: "MONTH",
  },
  {
    text: "Year",
    value: "YEAR",
  },
  {
    text: "All Time",
    value: "ALLTIME",
  },
];

export const mapDateBinToTimescaleUnit = (datebin) => {
  //https://www.chartjs.org/docs/latest/axes/cartesian/time.html#display-formats
  switch (datebin) {
    case "WEEK":
      return "day";
    case "MONTH":
      return "day";
    case "YEAR":
      return "month";
    case "ALLTIME":
      return "month";
  }
};
