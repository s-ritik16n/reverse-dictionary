import importlib.util as util

config_mod = util.spec_from_file_location('config','../config.py')
db_info = util.module_from_spec(config_mod)
config_mod.loader.exec_module(db_info)
dbinfo = db_info.db_info

cb_mod = util.spec_from_file_location('connect_db','/home/ritik/WORKSPACE/projects/reverse-dictionary/venv/src/data/connect_db.py')
cb = util.module_from_spec(cb_mod)
cb_mod.loader.exec_module(cb)
print_error = cb.print_error_import()
cb = cb.connect_db

from nltk.corpus import words
#from src.data.connect_db import connect_db as cb
#from src.data.print_error import print_error

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
else:
    print("Connection Error")
