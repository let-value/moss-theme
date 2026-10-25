// Verdant Meadow Theme — sage, olive and fresh leaf greens
import { readFile } from 'node:fs/promises';

const MEADOW_PALETTE = {
  leaf: '#C5E1A5',
  sage: '#90A479',
  olive: '#6C7B5A',
  pale: '#E4F1D6',
};

export class VerdantMeadow {
  constructor(name = 'Morning meadow') {
    this.name = name;
    this.palette = MEADOW_PALETTE;
  }

  /** Blend two meadow colors into a softer shade. */
  blend(from, to, ratio = 0.5) {
    const parse = (hex) =>
      [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16));
    const [a, b] = [parse(from), parse(to)];
    const mix = (value, i) =>
      Math.round(value * (1 - ratio) + b[i] * ratio);
    const toHex = (value) => value.toString(16).padStart(2, '0');
    return '#' + a.map(mix).map(toHex).join('');
  }

  async describe(file) {
    const content = await readFile(file, 'utf8');
    const lines = content.split('\n').filter(Boolean);
    return {
      name: this.name,
      shades: Object.keys(this.palette).length,
      lines: lines.length,
      content,
    };
  }
}

const theme = new VerdantMeadow();
const soft = theme.blend(MEADOW_PALETTE.sage, MEADOW_PALETTE.pale);

console.log(`soft meadow shade: ${soft}`);
