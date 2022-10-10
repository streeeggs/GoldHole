export class LineDataset {
  constructor(label, data, borderColor) {
    this.label = label ?? "Nothing here";
    this.data = data ?? [];
    this.borderColor = borderColor ?? "rgba(91, 100, 222, 0.4)"; // TODO: Import color instead
  }
}

export class LineChart {
  constructor(xAxisLabel, lineDatasets) {
    this.labels = xAxisLabel ?? [];
    this.datasets = lineDatasets ?? [new LineDataset()];
  }
}
