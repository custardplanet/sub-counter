from irc import IRC

import sqlite3


class SubCounter:

    def __init__(self, config):
        self.config = config
        irc = IRC()
        irc.connect(config['server'], config['port'], [config['channel']], config['nick'], config['oauth'])
        self.irc = irc

        conn = sqlite3.connect('subs.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS subs (username text, count integer)')
        cursor.execute('CREATE TABLE IF NOT EXISTS points (username text, count integer)')
        cursor.execute('CREATE TABLE IF NOT EXISTS votes (username text, option text, points integer)')
        cursor.close()
        conn.close()

        for option in config['options']:
            filename = 'counters/' + option.lower() + '.txt'
            try:
                f = open(filename, 'r')
            except:
                f = open(filename, 'w')
                f.write('0')

    def handle_sub_counter(self, event):
        conn = sqlite3.connect('subs.db')
        cursor = conn.cursor()

        cursor.execute('SELECT username, count FROM subs WHERE username = ?', (event['tags']['login'],))
        row = cursor.fetchone()

        if not row:
            cursor.execute('INSERT INTO subs VALUES (?, 1)', (event['tags']['login'],))
        else:
            cursor.execute('UPDATE subs SET count = count + 1 WHERE username = ?', (event['tags']['login'],))

            # compare post-incremented sub count
            if int(row[1] + 1) == int(self.config['subgoal']) and self.config['message']:
                print('someone gifted enough subs!')
                self.irc.send(self.config['channel'], self.config['message'].format(username=event['tags']['login']))

        conn.commit()
        cursor.close()
        conn.close

    def handle_sub_points(self, event):
        conn = sqlite3.connect('subs.db')
        cursor = conn.cursor()

        cursor.execute('SELECT username, count FROM points WHERE username = ?', (event['tags']['login'],))
        row = cursor.fetchone()

        if not row:
            cursor.execute('INSERT INTO points VALUES (?, 1)', (event['tags']['login'],))
        else:
            cursor.execute('UPDATE points SET count = count + 1 WHERE username = ?', (event['tags']['login'],))

        conn.commit()
        cursor.close()
        conn.close

    def handle_vote(self, event):
        conn = sqlite3.connect('subs.db')
        cursor = conn.cursor()

        username = event['tags']['display-name']

        cursor.execute('SELECT username, count FROM points WHERE username = ?', (username,))
        row = cursor.fetchone()

        if not row:
            self.irc.send(self.config['channel'], self.config['failed_vote_message'].format(username=username))
        else:
            choice = event['message'].split()[1]
            choice = choice.lower()

            if choice not in [option.lower() for option in self.config['options']]:
                self.irc.send(self.config['channel'], "Sorry, that's not an option! Please try again.")
                return

            points = int(row[1])
            cursor.execute('INSERT INTO votes VALUES (?, ?, ?)', (username, choice, points))
            cursor.execute('DELETE FROM points WHERE username = ?', (username,))
            conn.commit()

            with open('counters/' + choice + '.txt', 'r') as f:
                total = int(f.read())

            with open('counters/' + choice + '.txt', 'w') as f:
                f.write(str(total + points))

            self.irc.send(self.config['channel'], self.config['successful_vote_message'].format(option=choice))

            cursor.close()
            conn.close()

    def handle_admin_vote(self, event):
        # expected message format: !adminvote username option points
        conn = sqlite3.connect('subs.db')
        cursor = conn.cursor()

        msg = event['message'].split()
        username = msg[1].lower()
        choice = msg[2].lower()
        points = int(msg[3])

        if choice not in [option.lower() for option in self.config['options']]:
            self.irc.send(self.config['channel'], "Sorry, that's not an option! Please try again.")
            return

        cursor.execute('INSERT INTO votes VALUES (?, ?, ?)', (username, choice, points))
        conn.commit()

        self.irc.send(self.config['channel'], self.config['successful_vote_message'].format(option=choice))

        cursor.close()
        conn.close()

    def run_forever(self):
        while True:
            events = self.irc.read_events()

            for event in events:
                # uncomment for testing
                #if (event['code'] == 'PRIVMSG' and
                    #event['message'].startswith('!test')):
                    #event['tags']['login'] = 'spoongalaxy'

                if (event['code'] == 'USERNOTICE' and
                    'msg-id' in event['tags'] and
                    event['tags']['msg-id'] == 'subgift'):
                    #
                    self.handle_sub_counter(event)
                    self.handle_sub_points(event)
                elif (event['code'] == 'PRIVMSG' and
                      event['message'].startswith('!vote')):
                    self.handle_vote(event)
                elif (event['code'] == 'PRIVMSG' and
                      event['tags']['display-name'] in self.config['admins'] and
                      event['message'].startswith('!adminvote')):
                    self.handle_admin_vote(event)
