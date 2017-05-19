class _Storage:
    __keys = {}
    __values = {}

    @classmethod
    def _remove_value(cls, key, value):
        value = cls.__values.get(value, None)
        if value:
            if value[0]:
                value[0] -= 1
            value[1].discard(key)

    @classmethod
    def set(cls, key, value):
        old_value = cls.__keys.get(key, None)
        if old_value == value:
            return
        if old_value:
            cls._remove_value(key, old_value)
        cls.__keys[key] = value
        value = cls.__values.setdefault(value, [0, set()])
        value[0] += 1
        value[1].add(key)

    @classmethod
    def get(cls, key):
        return cls.__keys.get(key, 'NULL')

    @classmethod
    def unset(cls, key):
        if key in cls.__keys:
            cls._remove_value(key, cls.__keys.pop(key))

    @classmethod
    def counts(cls, value):
        value = cls.__values.get(value, None)
        return value[0] if value else 0

    @classmethod
    def find(cls, value):
        value = cls.__values.get(value, None)
        return value[1] if value else None


class DB:
    def __init__(self):
        self._transactions = []
