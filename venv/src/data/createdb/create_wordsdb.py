from data.config import dbinfo
from nltk.corpus import words
from ..connect_db import connect_db as cb
from ..print_error import print_error


def wordsdb(connection):
    total = 0
    try:
        for index,word in enumerate(words.words()):
            with connection.cursor() as cursor:
                sql = "INSERT INTO `words` (`id`,`word`) VALUES (%s, %s)"
                cursor.execute(sql, (index,word))
                connection.commit()
            total += 1
    except:
        print_error(err,"wordsdb")
        with connection.cursor() as cursor:
            sql = "DELETE * FROM `words`"
            cursor.execute(sql)
            connection.commit()
            print("data wiped")
    finally:
        print("rows inserted: ",total)
        connection.close()  

#connection = cb(dbinfo["user"], dbinfo["passwd"],"wordnetdb")
if connection is not None:
    #wordsdb(connection)
    print("sdf")
else:
    print("Connection returned None")
