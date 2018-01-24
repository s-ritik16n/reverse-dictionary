import MySQLdb as mysql
from print_error import print_error
from connect_db import connect_db as cb
from config import db_info
from nltk.corpus import wordnet as wn


def create_hypernyms(conn):
	try:
		cursor = conn.cursor(mysql.cursors.DictCursor)
		cursor.execute("SELECT  word, id from words group by word, id")
		result = cursor.fetchall()
		print(result)
		cursor.close()
		conn.commit()
		cursor = conn.cursor(mysql.cursors.DictCursor)
		for r in result:
			for word in wn.synsets(r["word"]):
				for hyper in word.hypernyms():
					if r["word"] == word.name().split('.')[0] and len(hyper.name()) > 0:
						cursor.execute("""INSERT INTO hypernyms (id, word, hypernym) VALUES ('{0}','{1}')""".format(r["id"], word.name().split('.')[0], hyper.name()))
						conn.commit()
		cursor.close()
		conn.close()
	except mysql.Error as e:
		print_error(e.args[1], "create_hypernyms")
		cursor = conn.cursor()
		cursor.execute("DELETE FROM hypernyms")
		conn.commit()
		cursor.close()
		conn.close()
conn = cb(user = db_info["user"], passwd = db_info["passwd"], db = "wordnetdb")
if conn is not None:
	create_hypernyms(conn)
else:
	print_error("Connection Error", "main -- create_hypernyms") 
