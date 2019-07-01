# The purpose of this script is to backup my OctoPrint Filament database each night.
# The database resides in a Postgres database on a Raspberry Pi Server.  Just in case something should happen to the
# server I won't loose any of my filament data.

import psycopg2
from configparser import ConfigParser

# Use ConfigParser to grab parameters from file
config = ConfigParser()
config.read('/home/pi/projects/FilamentDump/config.ini')
host = config.get('postgresql', 'host')
db = config.get('postgresql', 'database')
user = config.get('postgresql', 'user')
password = config.get('postgresql', 'password')


conn = psycopg2.connect(host=host, database=db, user=user, password=password)
cur = conn.cursor()
cur.execute('SELECT * FROM profiles')
listAll = cur.fetchall()
outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(listAll)
with open('profiles.txt', 'w') as f:
    cur.copy_expert(outputquery, f)
cur.execute('SELECT * FROM spools')
listAll = cur.fetchall()
outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(listAll)
with open('spools.txt', 'w') as f:
    cur.copy_expert(outputquery, f)
conn.close()

