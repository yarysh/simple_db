class _Storage:
    __storage = {}
    __storage_values_info = {}

    @classmethod
    def set(cls, key, value):
        cls.__storage[key] = value
        value_info = cls.__storage_values_info.setdefault(value, [0, set()])
        value_info[0] += 1
        value_info[1].add(key)

    @classmethod
    def get(cls, key):
        return cls.__storage.get(key, 'NULL')

    @classmethod
    def unset(cls, key):
        if key in cls.__storage:
            cls.__storage_values_info.pop(cls.__storage.pop(key), None)
            cls.__storage_values_info.pop(cls.__storage.pop(key), None)

    @classmethod
    def counts(cls, value):
        info = cls.__storage_values_info.get(value, None)  # type: dict
        return info[0] if info else 0

    @classmethod
    def find(cls, value):
        info = cls.__storage_values_info.get(value, None)  # type: dict
        return ', '.join(info[1]) if info else None


class DB:
    def __init__(self):
        self._transactions = []
