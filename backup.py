# The purpose of this script is to backup my OctoPrint Filament database each night.
# The database resides in a Postgres database on a Raspberry Pi Server.  Just in case something should happen to the
# server I won't loose any of my filament data.
# Author:  Mike Paxton
# Modified: 07/15/19

import psycopg2
from configparser import ConfigParser

# Use ConfigParser to grab parameters from file
config = ConfigParser()
config.read('/path/to//config.ini')
host = config.get('postgresql', 'host')
db = config.get('postgresql', 'database')
user = config.get('postgresql', 'user')
password = config.get('postgresql', 'password')
exportPath = config.get('default', 'exportPath')

conn = psycopg2.connect(host=host, database=db, user=user, password=password)
cur = conn.cursor()

sql = "COPY (SELECT * FROM profiles) TO STDOUT WITH CSV HEADER DELIMITER ','"
with open(exportPath + "profiles.csv", "w") as file:
    cur.copy_expert(sql, file)

sql = "COPY (SELECT * FROM spools) TO STDOUT WITH CSV HEADER DELIMITER ','"
with open(exportPath + "spools.csv", "w") as file:
    cur.copy_expert(sql, file)

cur.close()
conn.close()
