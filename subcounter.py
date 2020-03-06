from irc import IRC

import sqlite3


class SubCounter:

    def __init__(self, config):
        self.config = config
        self.irc = IRC.connect(config['server'], config['port'], [config['channel']], config['nick'], config['oauth'])

        conn = sqlite3.connect('subs.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS subs (username text, count integer)')
        cursor.close()
        conn.close()

    def handle_sub(self, event):
        conn = sqlite3.connect('subs.db')
        cursor = conn.cursor()

        cursor.execute('SELECT username, count FROM subs WHERE username = ?', (event['tags']['login'],))
        row = cursor.fetchone()

        if not row:
            cursor.execute('INSERT INTO subs VALUES (?, 1)', (event['tags']['login'],))
        else:
            cursor.execute('UPDATE subs SET count = count + 1 WHERE username = ?', (event['tags']['login'],))

            # compare post-incremented sub count
            if row[1] + 1 == self.config['subgoal']:
                self.irc.send(self.config['channel'], self.config['message'])

        conn.commit()
        cursor.close()
        conn.close

    def run_forever(self):
        while True:
            events = self.irc.read_events()

            for event in events:
                if (event['code'] == 'USERNOTICE' and
                    'msg-id' in event['tags'] and
                    event['tags']['msg-id'] == 'subgift':
                    #
                    self.handle_sub(event)
