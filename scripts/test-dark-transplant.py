import copy
import json
import math
from pathlib import Path
import subprocess
import unittest
from dark_transplant import ROOT, apply_transplants, plan, relative_color, hex_from_oklab, clusters


def theme():
    return dict(colors={}, semanticTokenColors={'string': '#657565'}, tokenColors=[
        dict(scope=['string.regexp'], settings=dict(foreground='#66756588')),
        dict(scope=['keyword'], settings=dict(foreground='#667565'))])


def config():
    return dict(semantic_distance=2, color_distance=6, roles=[
        dict(name='string', color='#DF7753', targets=['Semantic: string'])])


class TransplantTests(unittest.TestCase):
    def test_neighbor_bounds_and_alpha(self):
        base = theme()
        result, updates, _ = apply_transplants(base, config(), base)
        self.assertEqual(result['tokenColors'][0]['settings']['foreground'], '#DF775388')
        self.assertEqual(result['tokenColors'][1], base['tokenColors'][1])
        self.assertEqual(updates['TextMate: string.regexp']['kind'], 'neighbor')
        self.assertEqual(base, theme())
        for key in ('semantic_distance', 'color_distance'):
            cfg = config(); cfg[key] = 0
            self.assertNotIn('TextMate: string.regexp', plan(base, cfg)[0])

    def test_repeat_build_does_not_expand(self):
        baseline = theme()
        first, _, _ = apply_transplants(baseline, config(), baseline)
        second, _, _ = apply_transplants(first, config(), baseline)
        self.assertEqual(first, second)

    def test_explicit_target_wins(self):
        cfg = config()
        cfg['roles'].append(dict(name='regex', color='#AABBCC', targets=['TextMate: string.regexp']))
        result, _, _ = apply_transplants(theme(), cfg, theme())
        self.assertEqual(result['tokenColors'][0]['settings']['foreground'], '#AABBCC88')

    def test_ambiguous_neighbor_is_untouched(self):
        base = theme()
        base['semanticTokenColors']['string.escape'] = '#677565'
        cfg = config()
        cfg['roles'].append(dict(name='escape', color='#AABBCC', targets=['Semantic: string.escape']))
        result, updates, ambiguous = apply_transplants(base, cfg, base)
        self.assertNotIn('TextMate: string.regexp', updates)
        self.assertTrue(ambiguous)
        self.assertEqual(result['tokenColors'], base['tokenColors'])

    def test_const_bindings_are_gray_and_literals_stay_blue(self):
        baseline = json.loads((ROOT/'palette/dark-baseline.json').read_text())
        result, _, _ = apply_transplants(baseline)
        for key in ('variable', 'variable.readonly', 'parameter'):
            self.assertEqual(result['semanticTokenColors'][key], '#CACACA')
        self.assertEqual(result['semanticTokenColors']['number'], '#60CCFC')
        # Inspect every occurrence, so a hidden competing blue rule cannot pass.
        matches = {scope: [] for scope in ('variable.other.constant', 'constant.numeric', 'constant.language')}
        for rule in result['tokenColors']:
            for scope in rule['scope']:
                if scope in matches:
                    matches[scope].append(rule['settings']['foreground'])
        self.assertEqual(matches, {'variable.other.constant': ['#CACACA'],
                                  'constant.numeric': ['#60CCFC'], 'constant.language': ['#60CCFC']})
        again, _, _ = apply_transplants(result)
        self.assertEqual(result, again)

    def test_module_keywords_are_plain_and_wildcard_is_gray(self):
        baseline = json.loads((ROOT/'palette/dark-baseline.json').read_text())
        result, _, _ = apply_transplants(baseline)
        self.assertIs(result['semanticTokenColors']['keyword']['bold'], False)
        for scope in ('keyword.control.import', 'keyword.control.export', 'keyword.control.from'):
            rules = [r for r in result['tokenColors'] if scope in r['scope']]
            self.assertEqual(len(rules), 1)
            self.assertEqual(rules[0]['settings']['fontStyle'], '')
            self.assertEqual(rules[0]['settings']['foreground'], '#96C66C')
        wildcard = [r for r in result['tokenColors'] if 'constant.language.import-export-all' in r['scope']]
        self.assertEqual(len(wildcard), 1)
        self.assertEqual(wildcard[0]['settings']['foreground'], '#D4D1C8')
        numeric = [r for r in result['tokenColors'] if 'constant.numeric' in r['scope']]
        self.assertEqual(numeric[0]['settings']['foreground'], '#60CCFC')

    def test_bracket_colors_match_moss_and_have_punctuation_fallback(self):
        baseline = json.loads((ROOT/'palette/dark-baseline.json').read_text())
        result, _, _ = apply_transplants(baseline)
        moss = json.loads((ROOT.parent/'moss/vscode.json').read_text())
        keys = ['editorBracketHighlight.foreground'+str(i) for i in range(1, 7)]
        keys += ['editorBracketHighlight.unexpectedBracket.foreground',
                 'editorBracketMatch.background', 'editorBracketMatch.border',
                 'editorOverviewRuler.bracketMatchForeground']
        for key in keys:
            self.assertEqual(result['colors'][key].lower(), moss['colors'][key])
        for scope in ('punctuation.section', 'punctuation.definition.block',
                      'punctuation.definition.parameters', 'punctuation.definition.typeparameters'):
            rule = next(r for r in result['tokenColors'] if scope in r['scope'])
            self.assertEqual(rule['settings']['foreground'], '#D4D1C8')
        self.assertEqual(result['tokenColors'][0], baseline['tokenColors'][0])
        self.assertEqual(result, apply_transplants(result)[0])

    def test_string_delimiters_are_terracotta_and_code_braces_stay_gray(self):
        baseline = json.loads((ROOT/'palette/dark-baseline.json').read_text())
        result, _, _ = apply_transplants(baseline)
        for scope in ('punctuation.definition.string', 'punctuation.definition.template-expression',
                      'punctuation.section.interpolation'):
            rules = [r for r in result['tokenColors'] if scope in r['scope']]
            self.assertEqual(len(rules), 1)
            self.assertEqual(rules[0]['settings']['foreground'], '#DF7753')
        for scope in ('punctuation.definition.block', 'punctuation.section'):
            rule = next(r for r in result['tokenColors'] if scope in r['scope'])
            self.assertEqual(rule['settings']['foreground'], '#D4D1C8')
        self.assertEqual(result['semanticTokenColors']['variable'], '#CACACA')
        self.assertEqual(result['colors']['editorBracketHighlight.foreground1'], '#D4D1C8')
        self.assertEqual(result, apply_transplants(result)[0])

    def test_background_relative_shades_and_scope(self):
        baseline = json.loads((ROOT/'palette/dark-baseline.json').read_text())
        cfg = json.loads((ROOT/'palette/dark-transplants.json').read_text())
        original_cfg = copy.deepcopy(cfg)
        original_cfg['roles'] = [r for r in cfg['roles'] if r['name'] != 'editor-background']
        previous, _, _ = apply_transplants(baseline, original_cfg, baseline)
        result, updates, _ = apply_transplants(baseline, cfg, baseline)
        self.assertEqual(result['colors']['editor.background'], '#1F2F20')
        self.assertEqual(result['colors']['tab.activeBackground'], '#1F2F20')
        neighbors = {k:u for k,u in updates.items() if u['role']=='editor-background' and u['kind']=='neighbor'}
        self.assertGreater(len(neighbors), 40)
        self.assertGreater(len({u['color'] for u in neighbors.values()}), 15)
        old_seed = clusters.oklab(baseline['colors']['editor.background'])
        new_seed = clusters.oklab('#1F2F20')
        for token, update in neighbors.items():
            self.assertLessEqual(update['color_distance'], 24)
            self.assertLessEqual(update['semantic_distance'], 4)
            key = token.split(': ', 1)[1]
            actual = result['colors'][key]
            self.assertEqual(actual[7:], update['old'][7:])
            # RGB rounding allows a small error in the preserved perceptual offset.
            expected = tuple(o-s+n for o,s,n in zip(clusters.oklab(update['old']), old_seed, new_seed))
            self.assertLess(100*math.dist(clusters.oklab(actual), expected), .3)
        self.assertEqual(result['tokenColors'], previous['tokenColors'])
        self.assertEqual(result['semanticTokenColors'], previous['semanticTokenColors'])
        for key in previous['colors']:
            if key.startswith(('diffEditor.', 'editorGutter.', 'editorBracket')):
                self.assertEqual(result['colors'][key], previous['colors'][key])
        for key in ('editor.foreground','button.background','errorForeground','terminal.ansiRed'):
            self.assertEqual(result['colors'][key], previous['colors'][key])
        self.assertEqual(result, apply_transplants(result, cfg, baseline)[0])

    def test_oklab_roundtrip_and_gamut_handling(self):
        for color in ('#000000','#FFFFFF','#1F2F20','#FF0000','#00FF00','#0000FF'):
            self.assertEqual(hex_from_oklab(clusters.oklab(color)), color)
        self.assertEqual(relative_color('#232A20', '#232A20', '#1F2F20'), '#1F2F20')
        color = hex_from_oklab((.6, .8, -.5))
        lab = clusters.oklab(color)
        self.assertLess(abs(lab[0]-.6), .003)
        self.assertTrue(all(0 <= int(color[i:i+2], 16) <= 255 for i in (1,3,5)))

    def test_bottom_surfaces_match_editor(self):
        baseline = json.loads((ROOT/'palette/dark-baseline.json').read_text())
        result, _, _ = apply_transplants(baseline)
        for key in ('panel.background', 'terminal.background', 'statusBar.background', 'statusBar.noFolderBackground'):
            self.assertEqual(result['colors'][key], result['colors']['editor.background'])

    def test_real_migration_scope_and_sources(self):
        baseline = json.loads((ROOT/'palette/dark-baseline.json').read_text())
        cfg = json.loads((ROOT/'palette/dark-transplants.json').read_text())
        result, updates, _ = apply_transplants(baseline, cfg, baseline)
        moss = json.loads((ROOT.parent/'moss/vscode.json').read_text())
        self.assertEqual(result['colors']['editor.foreground'].lower(), moss['colors']['editor.foreground'])
        for key in ('number','keyword','function','method','type','class','interface','variable','parameter','property','operator','string'):
            value = result['semanticTokenColors'][key]
            self.assertEqual((value if isinstance(value, str) else value['foreground']).lower(), moss['semanticTokenColors'][key]['foreground'])
        self.assertEqual(result['semanticTokenColors']['variable.readonly'], '#CACACA')
        for key, value in baseline['colors'].items():
            if 'UI: '+key not in updates:
                self.assertEqual(result['colors'][key], value)
        self.assertEqual(result['tokenColors'][0], baseline['tokenColors'][0])  # Comments/styles.
        self.assertEqual(result, json.loads((ROOT/'themes/verdant-meadow-dark-color-theme.json').read_text()))
        light = 'themes/verdant-meadow-light-color-theme.json'
        self.assertEqual((ROOT/light).read_bytes(), subprocess.check_output(['git','-C',str(ROOT),'show','HEAD:'+light]))


if __name__ == '__main__':
    unittest.main()
