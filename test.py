import sqlite3


con = sqlite3.connect("data.db")
c = con.cursor()

# c.execute("INSERT INTO Person__model (__uid__, name, fullname, age) VALUES ('hash', 'Dima', 'Test', 18)")
# con.commit()

c.execute("SELECT * FROM Person__model WHERE name='Dima'")
print(c.fetchall())
