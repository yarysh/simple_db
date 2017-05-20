import unittest

from .db import _Storage, DB
from .exceptions import TransactionError


class Test_Storage(unittest.TestCase):
    def setUp(self):
        _Storage._Storage__keys.clear()
        _Storage._Storage__values.clear()

    def test_set(self):
        _Storage.set('A', 1)
        self.assertDictEqual({'A': 1}, _Storage._Storage__keys)
        self.assertDictEqual({1: {'A'}}, _Storage._Storage__values)

        _Storage.set('B', 1)
        self.assertDictEqual({'A': 1, 'B': 1}, _Storage._Storage__keys)
        self.assertDictEqual({1: {'A', 'B'}}, _Storage._Storage__values)

        _Storage.set('A', 'abc')
        self.assertDictEqual({'A': 'abc', 'B': 1}, _Storage._Storage__keys)
        self.assertDictEqual({1: {'B'}, 'abc': {'A'}}, _Storage._Storage__values)

    def test_get(self):
        _Storage._Storage__keys['A'] = 1
        self.assertEqual(1, _Storage.get('A'))

    def test_get_unknown_variable(self):
        self.assertEqual(_Storage.get('A'), 'NULL')

    def test_unset(self):
        _Storage._Storage__keys.update({'A': 1, 'B': 2, 'C': 1})
        _Storage._Storage__values.update({1: {'A', 'C'}, 2: {'B'}})
        _Storage.unset('A')
        self.assertDictEqual({'B': 2, 'C': 1}, _Storage._Storage__keys)
        self.assertDictEqual({1: {'C'}, 2: {'B'}}, _Storage._Storage__values)

    def test_unset_unknown_variable(self):
        self.assertNotIn('A', _Storage._Storage__keys)
        _Storage.unset('A')
        self.assertNotIn('A', _Storage._Storage__keys)

    def test_find(self):
        _Storage._Storage__keys.update({'A': 1, 'B': 2, 'C': 1})
        _Storage._Storage__values.update({1: {'A', 'C'}, 2: {'B'}})
        self.assertSetEqual({'A', 'C'}, _Storage.find(1))
        self.assertSetEqual({'B'}, _Storage.find(2))
        self.assertSetEqual(set(), _Storage.find(3))


class TestDB(unittest.TestCase):
    def setUp(self):
        _Storage._Storage__keys.clear()
        _Storage._Storage__values.clear()
        self.db = DB()

    def test_transaction_commit(self):
        self.db.begin()
        self.db.set('A', 1)
        self.assertEqual(1, self.db.get('A'))

        self.db.set('B', 2)
        self.db.unset('A')
        self.assertListEqual([[('A', 1), ('B', 2), ('A',)]], self.db._transactions)
        self.assertDictEqual({}, _Storage._Storage__keys)
        self.assertDictEqual({}, _Storage._Storage__values)
        self.assertEqual('NULL', self.db.get('A'))
        self.assertEqual(2, self.db.get('B'))

        self.db.commit()
        self.assertListEqual([], self.db._transactions)
        self.assertDictEqual({'B': 2}, _Storage._Storage__keys)
        self.assertDictEqual({2: {'B'}}, _Storage._Storage__values)
        self.assertEqual('NULL', self.db.get('A'))
        self.assertEqual(2, self.db.get('B'))

    def test_transaction_rollback(self):
        self.db.begin()
        self.db.set('A', 1)
        self.db.set('B', 2)
        self.db.set('A', 3)
        self.db.unset('C')
        self.assertListEqual([[('A', 1), ('B', 2), ('A', 3), ('C',)]], self.db._transactions)
        self.assertDictEqual({}, _Storage._Storage__keys)
        self.assertDictEqual({}, _Storage._Storage__values)
        self.assertEqual(3, self.db.get('A'))
        self.assertEqual(2, self.db.get('B'))
        self.assertEqual('NULL', self.db.get('C'))

        self.db.rollback()
        self.assertListEqual([], self.db._transactions)
        self.assertDictEqual({}, _Storage._Storage__keys)
        self.assertDictEqual({}, _Storage._Storage__values)
        self.assertEqual('NULL', self.db.get('A'))
        self.assertEqual('NULL', self.db.get('B'))
        self.assertEqual('NULL', self.db.get('C'))

    def test_inline_transaction_commit(self):
        self.db.begin()
        self.db.set('A', 1)
        self.db.set('B', 2)
        self.db.set('C', 3)
        self.db.set('E', 4)
        self.assertListEqual([[('A', 1), ('B', 2), ('C', 3), ('E', 4)]], self.db._transactions)

        self.db.begin()
        self.db.unset('A')
        self.db.set('B', 3)
        self.db.set('D', 4)
        self.assertListEqual([
            [('A', 1), ('B', 2), ('C', 3), ('E', 4)],
            [('A',), ('B', 3), ('D', 4)]
        ], self.db._transactions)
        self.assertDictEqual({}, _Storage._Storage__keys)
        self.assertDictEqual({}, _Storage._Storage__values)
        self.assertEqual('NULL', self.db.get('A'))
        self.assertEqual(3, self.db.get('B'))
        self.assertEqual(3, self.db.get('C'))
        self.assertEqual(4, self.db.get('D'))
        self.assertSetEqual({'B', 'C'}, self.db.find(3))

        self.db.commit()
        self.assertListEqual([[('A', 1), ('B', 2), ('C', 3), ('E', 4)]], self.db._transactions)
        self.assertDictEqual({'B': 3, 'D': 4}, _Storage._Storage__keys)
        self.assertDictEqual({3: {'B'}, 4: {'D'}}, _Storage._Storage__values)

        self.db.commit()
        self.assertListEqual([], self.db._transactions)
        self.assertDictEqual({'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 4}, _Storage._Storage__keys)
        self.assertDictEqual({1: {'A'}, 2: {'B'}, 3: {'C'}, 4: {'D', 'E'}}, _Storage._Storage__values)

    def test_inline_transaction_rollback(self):
        self.db.begin()
        self.db.set('A', 1)
        self.db.set('B', 2)
        self.assertEqual(1, self.db.get('A'))
        self.assertEqual(2, self.db.get('B'))

        self.db.begin()
        self.db.set('A', 2)
        self.db.set('B', 1)
        self.assertEqual(2, self.db.get('A'))
        self.assertEqual(1, self.db.get('B'))

        self.db.rollback()
        self.assertEqual(1, self.db.get('A'))
        self.assertEqual(2, self.db.get('B'))

        self.db.rollback()
        self.assertListEqual([], self.db._transactions)
        self.assertDictEqual({}, _Storage._Storage__keys)
        self.assertDictEqual({}, _Storage._Storage__values)

    def test_commit_when_no_transaction(self):
        with self.assertRaises(TransactionError):
            self.db.commit()

    def test_rollback_when_no_transaction(self):
        with self.assertRaises(TransactionError):
            self.db.rollback()
