from subcounter import SubCounter

import json

if __name__ == '__main__':
    with open('config.json') as f:
        config = json.load(f)

    bot = SubCounter(config)
    bot.run_forever()
