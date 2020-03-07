import sqlite3
import csv
import datetime

conn = sqlite3.connect('subs.db')
cursor = conn.cursor()

cursor.execute('select * from subs')
rows = cursor.fetchall()

timestamp = datetime.datetime.now()
filename = 'subs_' + timestamp.strftime('%Y%m%d-%H%M%S') + '.csv'

with open(filename, 'w', newline='') as out:
    writer = csv.writer(out)
    writer.writerow(['username', 'subs'])
    writer.writerows(rows)

cursor.close()
conn.close()
