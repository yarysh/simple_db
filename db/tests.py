import unittest

from .db import _Storage


class TestStorage(unittest.TestCase):
    def setUp(self):
        _Storage._Storage__keys.clear()
        _Storage._Storage__values.clear()

    def test_set(self):
        _Storage.set('A', 1)
        self.assertDictEqual({'A': 1}, _Storage._Storage__keys)
        self.assertDictEqual({1: [1, {'A'}]}, _Storage._Storage__values)

        _Storage.set('B', 1)
        self.assertDictEqual({'A': 1, 'B': 1}, _Storage._Storage__keys)
        self.assertDictEqual({1: [2, {'A', 'B'}]}, _Storage._Storage__values)

        _Storage.set('A', 'abc')
        self.assertDictEqual({'A': 'abc', 'B': 1}, _Storage._Storage__keys)
        self.assertDictEqual({1: [1, {'B'}], 'abc': [1, {'A'}]}, _Storage._Storage__values)

    def test_get(self):
        _Storage._Storage__keys['A'] = 1
        self.assertEqual(1, _Storage.get('A'))

    def test_get_unknown_variable(self):
        self.assertEqual(_Storage.get('A'), 'NULL')

    def test_unset(self):
        _Storage._Storage__keys.update({'A': 1, 'B': 2, 'C': 1})
        _Storage._Storage__values.update({1: [2, {'A', 'C'}], 2: [1, {'B'}]})
        _Storage.unset('A')
        self.assertDictEqual({'B': 2, 'C': 1}, _Storage._Storage__keys)
        self.assertDictEqual({1: [1, {'C'}], 2: [1, {'B'}]}, _Storage._Storage__values)

    def test_unset_unknown_variable(self):
        self.assertNotIn('A', _Storage._Storage__keys)
        _Storage.unset('A')
        self.assertNotIn('A', _Storage._Storage__keys)

    def test_counts(self):
        _Storage._Storage__keys.update({'A': 1, 'B': 2, 'C': 1})
        _Storage._Storage__values.update({1: [2, {'A', 'C'}], 2: [1, {'B'}]})
        self.assertEqual(2, _Storage.counts(1))
        self.assertEqual(1, _Storage.counts(2))
        self.assertEqual(0, _Storage.counts(3))

    def test_find(self):
        _Storage._Storage__keys.update({'A': 1, 'B': 2, 'C': 1})
        _Storage._Storage__values.update({1: [2, {'A', 'C'}], 2: [1, {'B'}]})
        self.assertSetEqual({'A', 'C'}, _Storage.find(1))
        self.assertSetEqual({'B'}, _Storage.find(2))
        self.assertIsNone(_Storage.find(3))
