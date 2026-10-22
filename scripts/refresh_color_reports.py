"""Regenerate inventories and cluster analysis for both built themes."""
from collections import defaultdict
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def refresh_variant(variant):
    theme = json.loads((ROOT/f'themes/verdant-meadow-{variant}-color-theme.json').read_text())
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
    lines = [f'# {variant.title()} theme color digest', '',
             f'Generated from `themes/verdant-meadow-{variant}-color-theme.json`. Explicit assignments only; inherited VS Code defaults are outside this inventory.', '',
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
    lines += ['', f'{variant.title()} transplants live in `palette/{variant}-transplants.json`; baseline light/dark pairs live in `scripts/build-theme.py`. Run the builder to regenerate themes and all {variant} reports. See `{variant.upper()}-TRANSPLANTS.md` for neighbor decisions.', '']
    (ROOT/f'{variant.upper()}-COLOR-DIGEST.md').write_text('\n'.join(lines))
    subprocess.run([sys.executable, str(ROOT/'scripts/cluster-dark-colors.py'), '--variant', variant,
                    '--report', str(ROOT/f'{variant.upper()}-PALETTE-CLUSTERS.md'),
                    '--output', str(ROOT/f'{variant}-palette-clusters.json')], check=True, stdout=subprocess.DEVNULL)


def refresh():
    for variant in ('dark', 'light'):
        refresh_variant(variant)
    light, dark = [json.loads((ROOT/f'themes/verdant-meadow-{v}-color-theme.json').read_text()) for v in ('light','dark')]
    spec = ['# Verdant Meadow Theme color specification', '', '| VS Code region | Light | Dark |', '|---|---|---|']
    keys = dict.fromkeys([*dark['colors'], *light['colors']])
    spec += [f"| `{key}` | `{light['colors'].get(key, 'inherited')}` | `{dark['colors'].get(key, 'inherited')}` |" for key in keys]
    (ROOT/'COLOR-SPEC.md').write_text('\n'.join(spec) + '\n')


if __name__ == '__main__':
    refresh()
