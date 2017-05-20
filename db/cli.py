import sys
from six.moves import input

from .db import DB


class CLI:
    def __init__(self):
        self.db = DB()

    def _exec(self, command, *args):
        command = command.lower()
        if not command or command in ('end', 'exit', 'quit'):
            return sys.exit(0)
        method = getattr(self.db, command, None)
        return method(*args) if method else 'Unknown command'

    def _pretty_print(self, result):
        if result:
            print(', '.join(result) if type(result) in (set, list) else result)
        else:
            print('' if result != 0 else 0)

    def run(self):
        print('*** SimpleDB CLI (ver. 0.1) ***')
        while True:
            try:
                command = input('>>> ').strip().split()
                result = self._exec(command[0] if command else '', *command[1:])
                self._pretty_print(result)
            except Exception as error:
                print('Command error: %s' % error)
