"""Apply appendable dark color transplants and discover bounded neighbors.

Uses a frozen pre-transplant baseline so re-running never expands the migration.
Only explicit color declarations are written. Both bounds must pass against a seed;
no recursive expansion. Explicit targets win; ambiguous neighbors are reported.
"""
import argparse
import copy
import importlib.util
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('color_clusters', ROOT/'scripts/cluster-dark-colors.py')
clusters = importlib.util.module_from_spec(spec)
spec.loader.exec_module(clusters)


def declarations(theme):
    values = {e['use']: e['value'] for entries in clusters.inventory(theme).values() for e in entries}
    return values


def distances(left, right, values, role=None):
    aliases = (role or {}).get('semantic_paths', {})
    def paths(use):
        return [tuple(aliases[use].split('.'))] if use in aliases else clusters.paths_of(use)
    semantic = max(clusters.path_distance(a, b) for a in paths(left) for b in paths(right))
    color = 100 * math.dist(clusters.oklab(values[left]), clusters.oklab(values[right]))
    return semantic, color


def linear_rgb(lab):
    L, a, b = lab
    l = (L + .3963377774*a + .2158037573*b) ** 3
    m = (L - .1055613458*a - .0638541728*b) ** 3
    s = (L - .0894841775*a - 1.2914855480*b) ** 3
    return (4.0767416621*l - 3.3077115913*m + .2309699292*s,
            -1.2684380046*l + 2.6097574011*m - .3413193965*s,
            -.0041960863*l - .7034186147*m + 1.7076147010*s)


def hex_from_oklab(lab):
    # Out-of-gamut colors reduce chroma at fixed lightness/hue, rather than
    # clipping RGB channels independently. Final rounding is to 8-bit sRGB.
    L, a, b = lab
    L = max(0, min(1, L))
    rgb = linear_rgb((L, a, b))
    if not all(-1e-7 <= v <= 1+1e-7 for v in rgb):
        low, high = 0., 1.
        for _ in range(32):
            middle = (low+high)/2
            trial = linear_rgb((L, a*middle, b*middle))
            if all(0 <= v <= 1 for v in trial):
                low = middle
            else:
                high = middle
        rgb = linear_rgb((L, a*low, b*low))
    def encode(value):
        value = max(0, min(1, value))
        return round(255 * (12.92*value if value <= .0031308 else 1.055*value**(1/2.4)-.055))
    return '#' + ''.join(f'{encode(v):02X}' for v in rgb)


def relative_color(old, old_seed, new_seed):
    old_lab, seed_lab, new_lab = map(clusters.oklab, (old, old_seed, new_seed))
    return hex_from_oklab(tuple(c - s + n for c, s, n in zip(old_lab, seed_lab, new_lab)))


def plan(baseline, config):
    if (not math.isfinite(config['color_distance']) or config['color_distance'] < 0
            or not isinstance(config['semantic_distance'], int) or config['semantic_distance'] < 0):
        raise ValueError('Neighbor limits must be nonnegative and finite; path distance must be an integer')
    for role in config['roles']:
        if role.get('neighbor_strategy', 'flat') not in ('flat', 'relative-oklab'):
            raise ValueError('Unknown neighbor strategy: ' + role['name'])
        if not math.isfinite(role.get('color_distance', config['color_distance'])) or role.get('color_distance', config['color_distance']) < 0:
            raise ValueError('Invalid color distance: ' + role['name'])
        if not isinstance(role.get('semantic_distance', config['semantic_distance']), int) or role.get('semantic_distance', config['semantic_distance']) < 0:
            raise ValueError('Invalid semantic distance: ' + role['name'])
        if not re.fullmatch(r'#[0-9A-Fa-f]{6}', role['color']):
            raise ValueError('Transplant colors must be opaque RGB hex: ' + role['name'])
    values = declarations(baseline)
    # Resolve explicit subset selectors against baseline rules for seed distances.
    for role in config['roles']:
        for target in role['targets']:
            if target.startswith('TextMate: ') and target not in values:
                wanted = set(target.split(': ', 1)[1].split(', '))
                for rule in baseline['tokenColors']:
                    scopes = rule['scope'] if isinstance(rule['scope'], list) else [rule['scope']]
                    if wanted <= set(scopes):
                        values[target] = rule['settings']['foreground']
    owners = {}
    for role in config['roles']:
        for target in role['targets']:
            if target in owners:
                raise ValueError('Duplicate explicit target: ' + target)
            owners[target] = role
    updates = {target: dict(role=role['name'], color=role['color'], kind='explicit',
                           old=values.get(target), **({'font_style': role['font_style']} if 'font_style' in role else {}))
               for target, role in owners.items()}
    ambiguous = []
    for candidate, old in values.items():
        if candidate in owners:
            continue
        matches = []
        for role in config['roles']:
            seeds = [seed for seed in role['targets'] if seed in values]
            eligible = []
            for seed in seeds:
                semantic, color = distances(candidate, seed, values, role)
                if semantic <= role.get('semantic_distance', config['semantic_distance']) and color <= role.get('color_distance', config['color_distance']):
                    eligible.append((color, semantic, seed))
            if eligible:
                color, semantic, seed = min(eligible)
                replacement = relative_color(old, values[seed], role['color']) if role.get('neighbor_strategy') == 'relative-oklab' else role['color']
                matches.append(dict(role=role['name'], color=replacement, kind='neighbor',
                                    strategy=role.get('neighbor_strategy', 'flat'),
                                    old=old, seed=seed, semantic_distance=semantic, color_distance=color))
        if len({m['color'] for m in matches}) > 1:
            ambiguous.append(dict(token=candidate, candidates=matches))
        elif matches:
            updates[candidate] = matches[0]
    return updates, ambiguous


def apply_transplants(theme, config=None, baseline=None):
    config = config if config is not None else json.loads((ROOT/'palette/dark-transplants.json').read_text())
    baseline = baseline if baseline is not None else json.loads((ROOT/'palette/dark-baseline.json').read_text())
    updates, ambiguous = plan(baseline, config)
    result = copy.deepcopy(theme)
    for target, update in updates.items():
        kind, key = target.split(': ', 1)
        color = update['color'][:7] + (update['old'][7:] if update['old'] else '')
        if kind == 'UI':
            result['colors'][key] = color
        elif kind == 'Semantic':
            old = result['semanticTokenColors'].get(key)
            if isinstance(old, dict):
                old['foreground'] = color
            else:
                result['semanticTokenColors'][key] = color
            if 'font_style' in update:
                current = result['semanticTokenColors'][key]
                if isinstance(current, str):
                    current = {'foreground': current}
                    result['semanticTokenColors'][key] = current
                current['bold'] = 'bold' in update['font_style'].split()
        else:
            scopes = key.split(', ')
            found = False
            rebuilt = []
            for rule in result['tokenColors']:
                existing = rule['scope'] if isinstance(rule['scope'], list) else [rule['scope']]
                if set(scopes) <= set(existing):
                    found = True
                    selected = copy.deepcopy(rule)
                    selected['scope'] = scopes
                    selected['settings']['foreground'] = color
                    if 'font_style' in update:
                        selected['settings']['fontStyle'] = update['font_style']
                    rebuilt.append(selected)
                    remaining = [scope for scope in existing if scope not in scopes]
                    if remaining:
                        remainder = copy.deepcopy(rule)
                        remainder['scope'] = remaining
                        rebuilt.append(remainder)
                else:
                    rebuilt.append(rule)
            if not found:
                settings = dict(foreground=color)
                if 'font_style' in update:
                    settings['fontStyle'] = update['font_style']
                rebuilt.append(dict(scope=scopes, settings=settings))
            result['tokenColors'] = rebuilt
    return result, updates, ambiguous


def write_reports(theme):
    config = json.loads((ROOT/'palette/dark-transplants.json').read_text())
    _, updates, ambiguous = apply_transplants(theme)
    report = ['# Dark transplants', '',
              f"Neighbor limits: semantic tree distance ≤ {config['semantic_distance']}, OKLab × 100 distance ≤ {config['color_distance']}. Measured on `palette/dark-baseline.json` before migration; no recursive propagation.", '',
              '| Role | Moss color | Explicit targets | Neighbors |', '|---|---|---:|---:|']
    for role in config['roles']:
        report.append(f"| {role['name']} | `{role['color']}` | {len(role['targets'])} | {sum(u['role']==role['name'] and u['kind']=='neighbor' for u in updates.values())} |")
    report += ['', '## Relative palette roles', '']
    for role in config['roles']:
        if role.get('neighbor_strategy') == 'relative-oklab':
            report.append(f"- {role['name']}: path ≤ {role.get('semantic_distance', config['semantic_distance'])}, OKLab × 100 ≤ {role.get('color_distance', config['color_distance'])}. UI surfaces/structure use explicit semantic path aliases in the manifest. Each neighbor retains its pre-migration OKLab offset from the seed; alpha is preserved. Out-of-gamut results reduce chroma at fixed lightness/hue. Explicit transplants are protected.")
    report += ['', '## Neighbor decisions', '']
    neighbors = {key: value for key, value in updates.items() if value['kind'] == 'neighbor'}
    if not neighbors:
        report.append('No additional declarations satisfy both limits outside the explicit targets.')
    for key, u in neighbors.items():
        report.append(f"- `{key}`: `{u['old']}` → `{u['color'] + u['old'][7:]}` via `{u['seed']}`; path {u['semantic_distance']}, color {u['color_distance']:.2f}.")
    for item in ambiguous:
        report.append(f"- Kept `{item['token']}`: qualifies for conflicting transplant colors.")
    report += ['', '## Append another role', '',
               'Append a role to `palette/dark-transplants.json` with its name, pinned Moss color, source reference, and explicit token targets. Run `python3 scripts/build-theme.py`; it applies the manifest to dark only and regenerates this report and `dark-transplants.json`. Inspect neighbor decisions before using the theme. Adjust the two limits in the manifest as needed. A role may override them with its own `semantic_distance` and `color_distance`. Set `neighbor_strategy` to `relative-oklab` to preserve neighbor offsets around the new seed; `semantic_paths` supplies reviewed aliases for related UI surfaces. Other roles keep the default flat replacement strategy. The baseline stays fixed; adding roles does not use already migrated colors as new evidence.', '']
    (ROOT/'DARK-TRANSPLANTS.md').write_text('\n'.join(report))
    (ROOT/'dark-transplants.json').write_text(json.dumps(dict(config=config, updates=updates, ambiguous=ambiguous),indent=2)+'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    theme = json.loads((ROOT/'themes/verdant-meadow-dark-color-theme.json').read_text())
    write_reports(theme)
