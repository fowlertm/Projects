import sqlite3 as sq
db = sq.connect('pipeline_db')
db.execute("""
    CREATE TABLE stage(`abbrev` text, `stagename` text)
    """)

print('finished')

