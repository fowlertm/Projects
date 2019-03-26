import sqlite3 as sq
db = sq.connect('pipeline_db')
stage_name = 'console'
curs = db.execute(f"SELECT stagename FROM stage WHERE abbrev = '{stage_name}';")
print(curs.fetchone())
print('finished')