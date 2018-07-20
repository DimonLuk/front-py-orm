import sqlite3


con = sqlite3.connect("test.db")
c = con.cursor()

c.execute("""CREATE TABLE test (field1 text, field2 text);""")
con.commit()
