from .exceptions import TransactionError


class _Storage:
    __keys = {}
    __values = {}

    @classmethod
    def _remove_value(cls, key, value):
        value_data = cls.__values.get(value, None)
        if value_data:
            value_data.discard(key)
            if not value_data:
                del cls.__values[value]

    @classmethod
    def set(cls, key, value):
        old_value = cls.__keys.get(key, None)
        if old_value == value:
            return
        if old_value:
            cls._remove_value(key, old_value)
        cls.__keys[key] = value
        value = cls.__values.setdefault(value, set())
        value.add(key)

    @classmethod
    def get(cls, key):
        return cls.__keys.get(key, 'NULL')

    @classmethod
    def unset(cls, key):
        if key in cls.__keys:
            cls._remove_value(key, cls.__keys.pop(key))

    @classmethod
    def find(cls, value):
        keys = cls.__values.get(value, None)
        return keys.copy() if keys is not None else set()


class DB:
    def __init__(self):
        self._transactions = []

    def begin(self):
        self._transactions.append([])

    def commit(self):
        if not self._transactions:
            raise TransactionError('Transaction not started')
        for operation in self._transactions.pop():
            _Storage.unset(*operation) if len(operation) == 1 else _Storage.set(*operation)

    def rollback(self):
        if not self._transactions:
            raise TransactionError('Transaction not started')
        self._transactions.pop()

    def get(self, key):
        for transaction in reversed(self._transactions):
            for operation in reversed(transaction):
                if operation[0] == key:
                    return operation[1] if len(operation) == 2 else 'NULL'
        return _Storage.get(key)

    def set(self, key, value):
        if self._transactions:
            self._transactions[-1].append((key, value))
        else:
            _Storage.set(key, value)

    def unset(self, key):
        if self._transactions:
            self._transactions[-1].append((key,))
        else:
            _Storage.unset(key)

    def find(self, value):
        keys = _Storage.find(value)
        for transaction in self._transactions:
            for operation in transaction:
                if len(operation) == 1:
                    keys.discard(operation[0])
                elif len(operation) == 2 and operation[1] == value:
                    keys.add(operation[0])
        return keys

    def counts(self, value):
        return len(self.find(value))
