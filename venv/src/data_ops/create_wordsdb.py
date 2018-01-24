import config
from print_error import print_error
from nltk.corpus import words, stopwords
import MySQLdb as mysqldb
dbinfo = config.db_info

def wordsdb(conn):
	total = 0
	exclude_words = [w.lower() for w in stopwords.words('english')]
	try:
		cursor = conn.cursor()
		for word in words.words():
			if word.lower() not in exclude_words:
				sql = """INSERT INTO words (word) VALUES ('{0}')""".format(word.lower())
				cursor.execute(sql)
				total += 1
				print("rows inserted: {}".format(total))
				conn.commit()
		cursor.close()
		conn.commit()
		conn.close()
	except mysqldb.Error as e:
		print_error(e.args[1],"wordsdb")
		cursor = conn.cursor()
		sql = "DELETE FROM words"
		cursor.execute(sql)
		cursor.close()
		conn.commit()
		conn.close()
		print("data wiped")


connection = mysqldb.connect(host = "localhost", user = dbinfo["user"], passwd = dbinfo["passwd"], db = "wordnetdb")
if connection is not None:
	wordsdb(connection)
else:
    print("Connection Error")
