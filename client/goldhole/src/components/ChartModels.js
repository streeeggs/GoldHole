/**
  type: 'line',
  data: {
    datasets: [{
      data: [{x:'2016-12-25', y:20}, {x:'2016-12-26', y:10}]
    }]
  }
 */
export class LineDataset {
  constructor(label, dataLabelArr, borderColor) {
    this.label = label ?? "No label";
    this.data = dataLabelArr ?? [];
    this.borderColor = borderColor ?? "rgba(91, 100, 222, 0.4)"; // TODO: Import color from theme? instead
  }
}

export class LineChart {
  constructor(lineDatasets) {
    this.type = "line";
    this.datasets = lineDatasets ?? [new LineDataset()];
  }
}

export class BarDataset {
  constructor(dataLabelArr, borderColors, backgroundColors, labels) {
    this.type = "bar";
    this.backgroundColor = backgroundColors;
    this.borderColor = borderColors;
    this.borderWidth = 1;
    this.data = dataLabelArr;
    this.label = labels;
  }
}

export class BarChart {
  constructor(barDatasets) {
    this.datasets = [barDatasets] ?? [new BarDataset()];
  }
}
