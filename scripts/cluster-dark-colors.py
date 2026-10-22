#!/usr/bin/env python3
"""Inventory and complete-link clustering of explicit dark-theme RGB bases.

No dependencies. Analysis only; never rewrites themes. Distance = 100 * Euclidean
OKLab distance. Conversion: https://bottosson.github.io/posts/oklab/
"""
import argparse
from collections import defaultdict
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def oklab(color):
    rgb = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
    r, g, b = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in rgb]
    l = (.4122214708*r + .5363325363*g + .0514459929*b) ** (1/3)
    m = (.2119034982*r + .6806995451*g + .1073969566*b) ** (1/3)
    s = (.0883024619*r + .2817188376*g + .6299787005*b) ** (1/3)
    return (.2104542553*l + .7936177850*m - .0040720468*s,
            1.9779984951*l - 2.4285922050*m + .4505937099*s,
            .0259040371*l + .7827717662*m - .8086757660*s)


# Align equivalent semantic/TextMate names while retaining their hierarchy.
SEMANTIC_PATHS = {
    'number': 'constant.numeric', 'parameter': 'variable.parameter', 'property': 'variable.other.property',
    'method': 'entity.name.function', 'function': 'entity.name.function',
    'type': 'entity.name.type', 'class': 'entity.name.type', 'interface': 'entity.name.type',
    'variable.readonly': 'variable.other.constant',
}
SCOPE_ALIASES = {
    'constant.character.escape': 'string.escape',
    'support.function': 'entity.name.function', 'support.type': 'entity.name.type',
    'support.class': 'entity.name.type', 'support.variable.property': 'variable.other.property',
}


def paths_of(use):
    kind, key = use.split(': ', 1)
    if kind == 'UI':
        return [('ui', *key.split('.'))]
    if kind == 'Semantic':
        return [('syntax', *SEMANTIC_PATHS.get(key, key).split('.'))]
    return [('syntax', *SCOPE_ALIASES.get(scope, scope).split('.'))
            for scope in key.split(', ')]


def path_distance(left, right):
    """Tree edge count below a shared semantic ancestor; unrelated roots never merge."""
    common = 0
    for a, b in zip(left, right):
        if a != b:
            break
        common += 1
    # Sharing only 'ui' or 'syntax' does not establish a semantic relationship.
    if common < 2:
        return math.inf
    return len(left) + len(right) - 2 * common


def analyze(entries, threshold, mode='semantic', semantic_distance=2):
    declarations = sorted((dict(e, paths=paths_of(e['use'])) for es in entries.values() for e in es),
                          key=lambda e: (e['use'], e['value']))
    labs = [oklab(e['value']) for e in declarations]
    colors, semantics, scores = {}, {}, {}
    groups = {i: (i,) for i in range(len(declarations))}
    for i in groups:
        for j in groups:
            if i >= j:
                continue
            pair = (i, j)
            colors[pair] = 100 * math.dist(labs[i], labs[j])
            semantics[pair] = max(path_distance(a, b) for a in declarations[i]['paths']
                                  for b in declarations[j]['paths']) if mode == 'semantic' else 0
            # Only eligible pairs compete. Larger color difference merges later.
            scores[pair] = colors[pair] if semantics[pair] <= semantic_distance and colors[pair] <= threshold else math.inf
    while scores:
        (i, j), score = min(scores.items(), key=lambda item: (item[1], item[0]))
        if not math.isfinite(score):
            break
        groups[i] += groups.pop(j)
        for k in groups:
            if k == i:
                continue
            ik, jk = tuple(sorted((i, k))), tuple(sorted((j, k)))
            scores[ik] = max(scores[ik], scores[jk])
        scores = {pair: value for pair, value in scores.items() if j not in pair}
    result, replacements = [], []
    for members in groups.values():
        def cd(a, b):
            return colors[tuple(sorted((a, b)))] if a != b else 0
        representative = min(members, key=lambda a: (sum(cd(a, b) for b in members), declarations[a]['value']))
        color = declarations[representative]['value'][:7]
        bases = sorted({declarations[i]['value'][:7] for i in members})
        paths = sorted({'.'.join(path) for i in members for path in declarations[i]['paths']})
        result.append({
            'representative': color, 'role': ', '.join(paths), 'paths': paths,
            'derivations': len(bases) - 1, 'members': bases, 'declarations': len(members),
            'max_pair_distance': max(cd(a, b) for a in members for b in members),
            'max_semantic_distance': max((semantics[tuple(sorted((a, b)))] for a in members for b in members if a != b), default=0),
            'max_representative_distance': max(cd(representative, b) for b in members),
        })
        for i in members:
            entry = declarations[i]
            replacements.append(dict(entry, replacement=color + entry['value'][7:]))
    return sorted(result, key=lambda g: (-g['declarations'], g['role'], g['representative'])), replacements


def inventory(theme):
    entries = defaultdict(list)
    def add(value, use):
        entries[value[:7].upper()].append({'value': value.upper(), 'use': use})
    for key, value in theme['colors'].items():
        add(value, 'UI: ' + key)
    for key, value in theme.get('semanticTokenColors', {}).items():
        add(value if isinstance(value, str) else value['foreground'], 'Semantic: ' + key)
    for rule in theme.get('tokenColors', []):
        # Count one declaration per rule, regardless of how many scopes it covers.
        if 'foreground' in rule['settings']:
            scopes = rule['scope']
            add(rule['settings']['foreground'], 'TextMate: ' + (scopes if isinstance(scopes, str) else ', '.join(scopes)))
    return dict(entries)


def cluster(entries, threshold):
    colors = sorted(entries)
    labs = {c: oklab(c) for c in colors}
    distances = {(a, b): 100 * math.dist(labs[a], labs[b]) for a in colors for b in colors}
    groups = [(c,) for c in colors]
    while len(groups) > 1:
        # Complete linkage bounds every pair, preventing chains of small steps
        # from joining perceptually distant endpoints. Sorted tuples break ties.
        distance, i, j = min((max(distances[a, b] for a in left for b in right), i, j)
                            for i, left in enumerate(groups) for j, right in enumerate(groups) if i < j)
        if distance > threshold:
            break
        merged = tuple(sorted(groups[i] + groups[j]))
        groups = sorted([g for k, g in enumerate(groups) if k not in (i, j)] + [merged])
    result = []
    for group in groups:
        # Weighted medoid: retain a real source color closest to all members,
        # weighted by declaration count. Frequency breaks equal-distance ties.
        representative = min(group, key=lambda a: (sum(distances[a, b]*len(entries[b]) for b in group), -len(entries[a]), a))
        result.append({
            'representative': representative,
            'derivations': len(group) - 1,
            'members': list(group),
            'declarations': sum(len(entries[c]) for c in group),
            'max_pair_distance': max(distances[a, b] for a in group for b in group),
            'max_representative_distance': max(distances[representative, c] for c in group),
        })
    return sorted(result, key=lambda g: (-g['declarations'], -g['derivations'], g['representative']))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--color-distance', '--threshold', dest='threshold', type=float, default=6, help='Maximum pairwise OKLab distance × 100 in a bundle (default: 6). Higher merges more.')
    parser.add_argument('--semantic-distance', type=int, default=2, help='Maximum tree edges between token paths (default: 2); unrelated roots never merge')
    parser.add_argument('--mode', choices=('semantic', 'perceptual'), default='semantic', help='Constrain token-path distance (default), or across all roles for comparison only')
    parser.add_argument('--theme', type=Path, default=ROOT/'themes/verdant-meadow-dark-color-theme.json')
    parser.add_argument('--output', type=Path, help='Write full machine-readable inventory, groups and replacement map as JSON')
    parser.add_argument('--report', type=Path, help='Write compact Markdown digest')
    args = parser.parse_args()
    if not math.isfinite(args.threshold) or args.threshold < 0:
        parser.error('--threshold must be finite and nonnegative')
    if args.semantic_distance < 0:
        parser.error('--semantic-distance must be nonnegative')
    entries = inventory(json.loads(args.theme.read_text()))
    groups, replacements = analyze(entries, args.threshold, args.mode, args.semantic_distance)
    report = ['# Dark palette clusters', '',
              f'{len(entries)} RGB bases → {len(groups)} role/color bundles at threshold {args.threshold:g} ({args.mode} mode, semantic distance {args.semantic_distance}).', '',
              'Distance: Euclidean OKLab × 100; complete linkage limits every pair in a bundle. Representatives are existing colors chosen by a declaration-weighted medoid. Sorted by declaration count (a usage proxy, not screen area). Derivations exclude the representative; singleton colors have zero.', '',
              'A merge must satisfy both limits for every pair of declarations. Semantic distance counts tree edges after the shared path prefix: string → string.regexp is 1, string.escape → string.regexp is 2. Unrelated roots never merge. UI and syntax are separate namespaces. Equivalent semantic/TextMate paths and string escapes have explicit aliases in the script. Multi-scope rules remain atomic and all their paths must qualify. Perceptual mode disables the path constraint for comparison.', '',
              'Alpha is excluded from RGB clustering and preserved in the proposed replacement map. These are base-color similarities, not composited on-screen similarities. This report does not modify themes.', '',
              '| Role | Main color | Derivations | Declarations | Maximum pair distance | Maximum path distance |',
              '|---|---|---:|---:|---:|---:|']
    report += [f"| {g['role']} | `{g['representative']}` | {g['derivations']} | {g['declarations']} | {g['max_pair_distance']:.2f} | {g['max_semantic_distance']} |" for g in groups]
    report += ['', 'Control: `python3 scripts/cluster-dark-colors.py --semantic-distance 2 --color-distance 6`. Lower values keep more distinctions; higher values merge more. Threshold 0 keeps all distinct RGB bases. Path distance 0 permits only identical canonical paths; 1 permits parent/child; 2 also permits siblings. Colors must independently pass the OKLab limit. Derivation counts describe geometric grouping, not source provenance.', '',
               'Conversion reference: https://bottosson.github.io/posts/oklab/', '']
    print('\n'.join(report))
    if args.report:
        args.report.write_text('\n'.join(report))
    if args.output:
        args.output.write_text(json.dumps({'mode': args.mode, 'color_distance': args.threshold, 'semantic_distance': args.semantic_distance, 'distance': '100 * Euclidean OKLab', 'rgb_bases': len(entries), 'clusters': groups, 'replacements_by_token': replacements, 'inventory': entries}, indent=2) + '\n')


if __name__ == '__main__':
    main()
