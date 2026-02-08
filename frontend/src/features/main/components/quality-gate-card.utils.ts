const METRIC_NAMES: Record<string, string> = {
  new_coverage: "Coverage",
  new_duplicated_lines_density: "Duplicated Lines",
  new_reliability_rating: "Reliability",
  new_security_rating: "Security",
  new_maintainability_rating: "Maintainability",
};

export function humanizeMetricKey(key: string): string {
  if (METRIC_NAMES[key]) return METRIC_NAMES[key];
  return key
    .replace(/^new_/, "")
    .replaceAll("_", " ")
    .replaceAll(/\b\w/g, (c) => c.toUpperCase());
}

export function formatThreshold(
  comparator: "LT" | "GT",
  threshold: string,
): string {
  const symbol = comparator === "LT" ? "\u2265" : "\u2264";
  return `${symbol} ${threshold}%`;
}
