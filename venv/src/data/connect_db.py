import pymysql.cursors as mysql
import pymysql
from print_error import print_error

def connect_db(user, passwd, db):
    connection = None
    try:
        connection = pymysql.connect(host = 'localhost', user=user, password = passwd, db=db, charset='utf8mb4', cursorclass=mysql.DictCursor)
    except pymysql.err.InternalError as err:
        print_error(err,"connect_db")
    except Exception as err:
        print_error(err,"connect_db")
    return connection

