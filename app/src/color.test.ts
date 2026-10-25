import { expect, it } from "vite-plus/test";
import { color } from "./color";

it.each([
  ["#f00", "#ff0000"],
  ["#FF0000ff", "#ff0000"],
  ["rgb(255, 0, 0)", "#ff0000"],
  ["rgb(255 0 0 / 50%)", "#ff000080"],
  ["oklch(0 0 0 / .5)", "#00000080"],
  ["oklch(1 0 0)", "#ffffff"],
  ["color(srgb 2 -1 0.5 / .5)", "#ff008080"],
])("normalizes %s to %s", (input, expected) => expect(color(input)).toBe(expected));

it.each(["", "not a color", "var(--color)", "currentColor", "rgb(NaN 0 0)"])(
  "rejects an invalid or context-dependent color: %s",
  (input) => expect(() => color(input)).toThrow("Invalid color"),
);
