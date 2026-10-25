import { converter, formatHex8 } from "culori";

const rgb = converter("rgb");

// Convert to sRGB and clip each channel to its displayable range, including alpha.
export function color(value: string): string {
  const parsed = rgb(value);
  if (!parsed || ![parsed.r, parsed.g, parsed.b, parsed.alpha ?? 1].every(Number.isFinite)) {
    throw new Error(`Invalid color: ${value}`);
  }
  const hex = formatHex8(parsed);
  return hex.endsWith("ff") ? hex.slice(0, 7) : hex;
}
