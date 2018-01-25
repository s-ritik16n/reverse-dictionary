#!/usr/bin/env python3

import importlib.util as util
import MySQLdb as mysqldb
import os, sys
from print_error import print_error
from sqlalchemy import create_engine, MetaData

def connect_db(user, passwd, db):
    connection = None
    try:
        connection = mysqldb.connect(host = 'localhost', user=user, password = passwd, db=db)
    except mysqldb.Error as e:
        print_error(e.args[1],"connect_db")
    except Exception as err:
        print_error(err,"connect_db")
    return connection

def get_engine():
	engine = create_engine("mysql+mysqldb://root:"+'2340532'+"@localhost/wordnetdb")
	meta = MetaData(bind=engine)
	return engine, meta
