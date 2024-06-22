#https//docs.python.org/3/library/sqlite3.html
import sqlite3
con = sqlite3.connect("files_data.db")
cur = con.cursor()
cur.execute("CREATE TABLE if not exists file_meta_data(Name, Size, Item_Type, Date_Modified, Date_Created, Full_Path, Path, md5)")
res = cur.execute("SELECT * FROM file_meta_data")
print(res.fetchone())