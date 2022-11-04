import { LineChart, LineDataset } from "./ChartModels";

/*
 * Just need to map shit that comes back from the API to whatever chart.js expects
 * Also controls some common styling elements in shitty way since I'm currently styling each chart instead of styling globally
 * Probably best to have a seperate collection of functions to hanlde that or, you know, do it right with global styling
 */

export const coulmnToDataset = (
  json,
  label_col,
  data_col,
  generate_colors = false,
  seperate_labels = false
) => {
  const colors = generate_colors
    ? generateColors(blue_dark, blue_light, json.length)
    : ([], []);
  let res = {
    labels: [],
    datasets: [
      {
        data: [],
        backgroundColor: colors[0],
        borderColor: colors[1],
        borderWidth: 1,
      },
    ],
  };
  // Some charts (eg: Pie) require data and labels to be seperated. See https://www.chartjs.org/docs/latest/charts/doughnut.html
  if (seperate_labels) {
    res.datasets[0].data = json.map((d) => d[data_col]);
    res.labels = json.map((d) => shortenLabel(d[label_col]));
  } else {
    res.datasets[0].data = json.reduce(
      (acc, curr) => ({
        ...acc,
        [shortenLabel(curr[label_col])]: curr[data_col],
      }),
      {}
    );
  }
  return res;
};

export const objectToDataset = (json, generate_colors = false) => {
  const colors = generate_colors
    ? generateColors(blue_dark, blue_light, Object.keys(json).length)
    : ([], []);
  let res = {
    datasets: [
      {
        label: "",
        data: [],
        backgroundColor: generate_colors ? colors[0] : "",
        borderColor: generate_colors ? colors[1] : "",
        borderWidth: 1,
      },
    ],
  };
  res.datasets[0].data = json; // TODO: Function should be more agnostic to multiple datasets; not just one
  return res;
};

/**
 * Mapper for "/users that builds datasets for each user.
 * Result is for a LineChart.
 * @param {Object} json API response from date range user. Expects a shape of [{"date", "user", "favor"}]
 * @returns {LineChart}
 */
export const mapUserDataResultToLine = (json) => {
  const dataSets = [];
  const user = json.user;
  // Need a set to ensure we have each possible x-axis date bin for each user we're creating a line for
  let uniqueDates = new Set();
  for (let date of json.dates) {
    uniqueDates.add(date.date);
    dataSets.push(new LineDataset(user, date.favor));
    // TODO: figure out who's 1st 2nd and 3rd so you can give them their own colors
  }
  return new LineChart([...uniqueDates], dataSets);
};

// Start of ugly string manip... TODO: Move to own file?

const MAX_LABEL_LEN = 20;
/**
 * Shorten a given label
 * @param {String} str
 * @returns Shorten label if over max length
 */
const shortenLabel = (str) =>
  str.length < MAX_LABEL_LEN
    ? str
    : str.substring(0, str.lastIndexOf(" ", MAX_LABEL_LEN));

const blue_dark = "rgba(91, 100, 222, 0.4)";
const blue_light = "rgba(91, 192, 222, 0.4)";
const rbga_reg =
  /^rgba\s*\(\s*([\d.]+%?)\s*,\s*([\d.]+%?)\s*,\s*([\d.]+%?)\s*(,\s*([\d.]+%?))?\)$/;

/**
 * Generate a random color between two given values
 * @param {Number} c1
 * @param {Number} c2
 * @returns New color between two
 */
const randomColor = (c1, c2) => c1 + Math.floor((c2 - c1) * Math.random());

/**
 * Map an rgba string into an object
 * @param {String} color_str
 * @returns Color object
 */
const getValue = (color_str) => ({
  red: `${color_str.replace(rbga_reg, "$1")}`,
  green: `${color_str.replace(rbga_reg, "$2")}`,
  blue: `${color_str.replace(rbga_reg, "$3")}`,
  alpha: `${color_str.replace(rbga_reg, "$5")}`,
});

/**
 * Generate an array of colors between two given values. Partially stolen from https://stackoverflow.com/a/42178175
 * @param {String} color1
 * @param {String} color2
 * @param {Number} size
 * @returns An array of two arrays; One for all background colors (alpha) and one for all borders (no alpha)
 */
const generateColors = (color1, color2, size) => {
  let background = [],
    border = [];
  const c1 = getValue(color1),
    c2 = getValue(color2);
  for (let i = 0; i < size; i++) {
    let red = randomColor(Number(c1.red), Number(c2.red)),
      green = randomColor(Number(c1.green), Number(c2.green)),
      blue = randomColor(Number(c1.blue), Number(c2.blue)),
      alpha = c1.alpha;
    background.push(`rgba(${red}, ${green}, ${blue}, ${alpha})`);
    border.push(`rgba(${red}, ${green}, ${blue}, 1)`);
  }
  return [background, border];
};
