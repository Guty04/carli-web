const ACCESS_LEVEL_MAP: Record<number, string> = {
  10: "Guest",
  20: "Reporter",
  30: "Developer",
  40: "Maintainer",
  50: "Owner",
};

export function mapAccessLevelToRole(level: number): string {
  return ACCESS_LEVEL_MAP[level] ?? "Unknown";
}
