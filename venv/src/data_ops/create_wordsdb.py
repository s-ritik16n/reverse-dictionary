#import importlib.util as util

import config
dbinfo = config.db_info

from connect_db import connect_db as cb
from print_error import print_error
from nltk.corpus import words

def wordsdb(connection):
    total = 0
    try:
        for index,word in enumerate(words.words()):
            with connection.cursor() as cursor:
                sql = "INSERT INTO `words` (`word`) VALUES (%s)"
                cursor.execute(sql, (word))
                connection.commit()
            total += 1
            print("rows inserted: ",total)
    except Exception as err:
        print_error(err,"wordsdb")
        with connection.cursor() as cursor:
            sql = "DELETE FROM `words`"
            cursor.execute(sql)
            connection.commit()
            print("data wiped")


connection = cb(dbinfo["user"], dbinfo["passwd"],"wordnetdb")
if connection is not None:
	wordsdb(connection)
	pass
else:
    print("Connection Error")
