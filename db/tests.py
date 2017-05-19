import unittest

from .db import _Storage


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.storage = _Storage._Storage__storage  # type: dict
        self.storage.clear()
        _Storage._Storage__storage_values_info.clear()

    def test_set_variable(self):
        _Storage.set('A', 1)
        self.assertEqual(self.storage['A'], 1)
        _Storage.set('A', 'abc')
        self.assertEqual(self.storage['A'], 'abc')

    def test_get_variable(self):
        self.storage['A'] = 1
        self.assertEqual(_Storage.get('A'), 1)

    def test_get_unknown_variable(self):
        self.assertEqual(_Storage.get('A'), 'NULL')

    def test_unset_variable(self):
        self.storage['A'] = 1
        _Storage.unset('A')
        self.assertNotIn('A', self.storage)

    def test_unset_unknown_variable(self):
        self.assertNotIn('A', self.storage)
        _Storage.unset('A')
        self.assertNotIn('A', self.storage)

    def test_counts(self):
        _Storage.set('A', 1)
        _Storage.set('B', 2)
        _Storage.set('C', 1)
        _Storage.set('D', '1')
        self.assertEqual(_Storage.counts(1), 2)
        self.assertEqual(_Storage.counts('1'), 1)
        self.assertEqual(_Storage.counts(2), 1)
        self.assertEqual(_Storage.counts(3), 0)

    def test_find(self):
        _Storage.set('A', 1)
        _Storage.set('B', 2)
        _Storage.set('C', 1)
        _Storage.set('D', '1')
        self.assertEqual(_Storage.find(1), 'A, C')
        self.assertEqual(_Storage.find('1'), 'D')
        self.assertEqual(_Storage.find(2), 'B')
        self.assertEqual(_Storage.counts(3), 0)
