import sqlite3


con = sqlite3.connect("data.db")
c = con.cursor()

c.execute("SELECT * FROM Person__model WHERE name='Dima'")
print(c.fetchall())
