#!/usr/bin/env python


if __name__ == '__main__':
    from db import CLI
    try:
        CLI().run()
    except KeyboardInterrupt:
        pass
    except Exception:
        print('SimpleDB unknown exception...')
