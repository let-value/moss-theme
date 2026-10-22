"""Regression checks for the light migration and its generated neighbors."""
import copy
import json
import math
import subprocess
import unittest
from dark_transplant import ROOT, apply_transplants, clusters


class LightTransplantTests(unittest.TestCase):
    def setUp(self):
        self.base = json.loads((ROOT/'palette/light-baseline.json').read_text())
        self.config = json.loads((ROOT/'palette/light-transplants.json').read_text())
        self.source = json.loads((ROOT/'palette/moss-light-source.json').read_text())
        self.theme, self.updates, self.ambiguous = apply_transplants(self.base, self.config, self.base)

    def rule(self, scope):
        matches = [r for r in self.theme['tokenColors'] if scope in r['scope']]
        self.assertEqual(len(matches), 1, scope)
        return matches[0]['settings']

    def test_moss_source_and_syntax(self):
        self.assertEqual(self.theme['colors']['editor.foreground'], '#1E1C18')
        for key in ('number','keyword','function','method','type','class','interface',
                    'variable','parameter','property','operator','string'):
            value = self.theme['semanticTokenColors'][key]
            self.assertEqual(value['foreground'] if isinstance(value, dict) else value,
                             self.source['semanticTokenColors'][key])
        self.assertEqual(self.rule('string')['foreground'], '#933814')
        self.assertEqual(self.rule('constant.numeric')['foreground'], '#005E86')
        self.assertEqual(self.rule('entity.name.function')['foreground'], '#63501F')

    def test_const_and_destructured_bindings_are_neutral(self):
        for key in ('variable', 'variable.readonly', 'parameter'):
            self.assertEqual(self.theme['semanticTokenColors'][key], '#1D1D1D')
        for scope in ('variable', 'variable.other.constant', 'variable.parameter'):
            self.assertEqual(self.rule(scope)['foreground'], '#1D1D1D')

    def test_keywords_are_plain_and_wildcard_is_gray(self):
        self.assertIs(self.theme['semanticTokenColors']['keyword']['bold'], False)
        for scope in ('keyword.control.import','keyword.control.export','keyword.control.from'):
            self.assertEqual(self.rule(scope), dict(foreground='#3B6305', fontStyle=''))
        self.assertEqual(self.rule('constant.language.import-export-all')['foreground'], '#1E1C18')
        self.assertEqual(self.rule('constant.language')['foreground'], '#005E86')

    def test_brackets_string_delimiters_and_escape_neighbor(self):
        for i in range(1, 7):
            self.assertEqual(self.theme['colors']['editorBracketHighlight.foreground'+str(i)],
                             '#3F5B48' if i==4 else '#1E1C18')
        self.assertEqual(self.rule('punctuation.definition.block')['foreground'], '#1E1C18')
        for scope in ('punctuation.definition.string','punctuation.definition.template-expression',
                      'punctuation.section.interpolation','constant.character.escape'):
            self.assertEqual(self.rule(scope)['foreground'], '#933814')
        self.assertEqual(self.updates['TextMate: constant.character.escape']['kind'], 'neighbor')
        self.assertLessEqual(self.updates['TextMate: constant.character.escape']['color_distance'], 6)

    def test_bottom_surfaces_and_readable_status_text(self):
        for key in ('editor.background','panel.background','terminal.background',
                    'statusBar.background','statusBar.noFolderBackground'):
            self.assertEqual(self.theme['colors'][key], '#DAE2DA')
        for key in ('statusBar.foreground','statusBar.noFolderForeground'):
            self.assertEqual(self.theme['colors'][key], '#1E1C18')

    def test_relative_neighbors_alpha_and_boundaries(self):
        neighbors = {k:u for k,u in self.updates.items() if u['role']=='editor-background' and u['kind']=='neighbor'}
        self.assertGreater(len(neighbors), 40)
        self.assertGreater(len({u['color'] for u in neighbors.values()}), 15)
        old_seed = clusters.oklab(self.base['colors']['editor.background'])
        new_seed = clusters.oklab('#DAE2DA')
        for key, u in neighbors.items():
            actual = self.theme['colors'][key.split(': ',1)[1]]
            self.assertEqual(actual[7:], u['old'][7:])
            self.assertLessEqual(u['semantic_distance'], 4)
            self.assertLessEqual(u['color_distance'], 24)
            expected = tuple(c-s+n for c,s,n in zip(clusters.oklab(u['old']),old_seed,new_seed))
            self.assertLess(100*math.dist(clusters.oklab(actual),expected), .3)
        for key,value in self.base['colors'].items():
            if key.startswith(('diffEditor.','editorGutter.')):
                self.assertEqual(self.theme['colors'][key],value)
        self.assertEqual(self.theme['tokenColors'][0],self.base['tokenColors'][0])
        self.assertFalse(self.ambiguous)

    def test_repeatability_and_dark_is_unchanged(self):
        self.assertEqual(self.theme,apply_transplants(self.theme,self.config,self.base)[0])
        self.assertEqual(self.theme,json.loads((ROOT/'themes/verdant-meadow-light-color-theme.json').read_text()))
        dark='themes/verdant-meadow-dark-color-theme.json'
        self.assertEqual((ROOT/dark).read_bytes(),subprocess.check_output(['git','-C',str(ROOT),'show','HEAD:'+dark]))


if __name__ == '__main__':
    unittest.main()
