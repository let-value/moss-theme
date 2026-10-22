"""Regenerate dark inventories from the built theme, including cluster analysis."""
from collections import defaultdict
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def refresh():
    theme = json.loads((ROOT/'themes/verdant-meadow-dark-color-theme.json').read_text())
    refs = defaultdict(list)
    for key, value in theme['colors'].items():
        refs[value].append('UI: ' + key)
    for key, value in theme['semanticTokenColors'].items():
        refs[value if isinstance(value, str) else value['foreground']].append('Semantic: ' + key)
    for rule in theme['tokenColors']:
        scopes = rule['scope'] if isinstance(rule['scope'], list) else [rule['scope']]
        refs[rule['settings']['foreground']].extend('TextMate: ' + scope for scope in scopes)
    syntax = {rule['settings']['foreground'] for rule in theme['tokenColors']} | {
        value if isinstance(value, str) else value['foreground'] for value in theme['semanticTokenColors'].values()}
    lines = ['# Dark theme color digest', '',
             'Generated from `themes/verdant-meadow-dark-color-theme.json`. Explicit assignments only; inherited VS Code defaults are outside this inventory.', '',
             f"- {len(refs)} distinct hex values; {sum(len(c)==7 for c in refs)} opaque, {sum(len(c)==9 for c in refs)} translucent.",
             f"- {len({c[:7] for c in refs})} RGB bases when alpha is ignored.",
             f"- {len(theme['colors'])} UI declarations, {len(theme['semanticTokenColors'])} semantic declarations, {len(theme['tokenColors'])} TextMate rules.",
             f'- {len(syntax)} syntax colors.', '', '## Syntax', '', '| Scopes | Color |', '|---|---|']
    for rule in theme['tokenColors']:
        scopes = rule['scope'] if isinstance(rule['scope'], list) else [rule['scope']]
        lines.append('| '+', '.join('`'+s+'`' for s in scopes)+' | `'+rule['settings']['foreground']+'` |')
    lines += ['', '## Complete inventory', '', '| Color | Uses |', '|---|---|']
    for color, uses in sorted(refs.items()):
        lines.append('| `'+color+'` | '+'; '.join('`'+use+'`' for use in uses)+' |')
    lines += ['', 'Dark transplants live in `palette/dark-transplants.json`; baseline light/dark pairs live in `scripts/build-theme.py`. Run the builder to regenerate themes and all dark reports. See `DARK-TRANSPLANTS.md` for neighbor decisions.', '']
    (ROOT/'DARK-COLOR-DIGEST.md').write_text('\n'.join(lines))
    light = json.loads((ROOT/'themes/verdant-meadow-light-color-theme.json').read_text())
    spec = ['# Verdant Meadow Theme color specification', '', '| VS Code region | Light | Dark |', '|---|---|---|']
    spec += [f"| `{key}` | `{light['colors'].get(key, 'inherited')}` | `{value}` |" for key, value in theme['colors'].items()]
    (ROOT/'COLOR-SPEC.md').write_text('\n'.join(spec) + '\n')
    subprocess.run([sys.executable, str(ROOT/'scripts/cluster-dark-colors.py'),
                    '--report', str(ROOT/'DARK-PALETTE-CLUSTERS.md'),
                    '--output', str(ROOT/'dark-palette-clusters.json')], check=True, stdout=subprocess.DEVNULL)


if __name__ == '__main__':
    refresh()
