
#!/usr/bin/env python
import sqlite3
conn = sqlite3.connect('test_db')
c = conn.cursor()
c.execute("""SELECT * FROM ROUNDS""")
joe = c.fetchall()
for row in joe:
    print row
