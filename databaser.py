import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, score TEXT);')

""" 
cursor.execute(f'''
    INSERT INTO records(name, score)
    VALUES(?,?)
''', ('FILLIPE', 50))
for row in cursor.execute('SELECT * FROM records'):
    print(row)
"""

conn.commit()

