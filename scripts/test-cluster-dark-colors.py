"""Run with python3 scripts/test-cluster-dark-colors.py."""
import importlib.util
import math
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('cluster', Path(__file__).with_name('cluster-dark-colors.py'))
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


class SemanticClusteringTests(unittest.TestCase):
    def test_shared_hex_is_scoped_by_declaration(self):
        entries = {
            '#DF7753': [{'value': '#DF7753', 'use': 'Semantic: string'}],
            '#DE7753': [{'value': '#DE7753', 'use': 'TextMate: string'},
                        {'value': '#DE775366', 'use': 'UI: button.background'}],
        }
        groups, replacements = c.analyze(entries, 100)
        self.assertEqual(len(groups), 2)
        string_groups = [g for g in groups if g['role'] == 'syntax.string']
        self.assertEqual(string_groups[0]['derivations'], 1)
        ui = next(r for r in replacements if r['use'].startswith('UI:'))
        self.assertEqual(ui['replacement'], '#DE775366')
        self.assertEqual(len(replacements), 3)

    def test_regex_and_escapes_never_spill(self):
        entries = {color: [{'value': color, 'use': use}] for color, use in [
            ('#DF7753', 'TextMate: string'),
            ('#DE7753', 'TextMate: constant.character.escape'),
            ('#DD7753', 'TextMate: string.regexp'),
            ('#DC7753', 'TextMate: keyword')]}
        self.assertEqual(len(c.analyze(entries, 100, semantic_distance=0)[0]), 4)
        self.assertEqual(len(c.analyze(entries, 100, 'perceptual')[0]), 1)

    def test_path_and_color_limits_are_independent(self):
        entries = {
            '#DF7753': [{'value': '#DF7753', 'use': 'TextMate: string'}],
            '#DE7753': [{'value': '#DE7753', 'use': 'TextMate: string.regexp'}],
        }
        self.assertEqual(len(c.analyze(entries, 6, semantic_distance=0)[0]), 2)
        self.assertEqual(len(c.analyze(entries, 6, semantic_distance=1)[0]), 1)
        self.assertEqual(len(c.analyze(entries, 0, semantic_distance=1)[0]), 2)

    def test_tree_edges_and_unrelated_roots(self):
        path = lambda key: c.paths_of('TextMate: ' + key)[0]
        self.assertEqual(c.path_distance(path('string'), path('string.regexp')), 1)
        self.assertEqual(c.path_distance(path('string.escape'), path('string.regexp')), 2)
        self.assertTrue(math.isinf(c.path_distance(path('string'), path('keyword'))))
        self.assertTrue(math.isinf(c.path_distance(path('string'), ('ui', 'string'))))

    def test_path_chains_do_not_bypass_pair_limit(self):
        entries = {'#DF7753': [{'value': '#DF7753', 'use': 'TextMate: ' + scope}
                              for scope in ('string', 'string.escape', 'string.regexp')]}
        groups, _ = c.analyze(entries, 6, semantic_distance=1)
        self.assertEqual(len(groups), 2)
        self.assertTrue(all(g['max_semantic_distance'] <= 1 for g in groups))

    def test_reference_conversion(self):
        self.assertLess(math.dist(c.oklab('#FF0000'), (.6279553606, .2248630611, .1258462985)), 1e-6)

    def test_no_distance_chaining(self):
        entries = {v: [{}] for v in ('#202020', '#282828', '#303030')}
        distance = lambda a, b: 100 * math.dist(c.oklab(a), c.oklab(b))
        limit = max(distance('#202020', '#282828'), distance('#282828', '#303030')) + .001
        groups = c.cluster(entries, limit)
        self.assertEqual(len(groups), 2)
        self.assertTrue(all(g['max_pair_distance'] <= limit for g in groups))


if __name__ == '__main__':
    unittest.main()
