import sqlite3


con = sqlite3.connect("data.db")
c = con.cursor()

c.execute("INSERT INTO Person__model(name, fullname, age) VALUES(?,?,?)", ("Dima", "Lukashov", 18))
con.commit()
con.close()
