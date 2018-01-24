#!/usr/bin/env python3

import importlib.util as util
import MySQLdb as mysqldb
import os, sys
from print_error import print_error

def connect_db(user, passwd, db):
    connection = None
    try:
        connection = mysqldb.connect(host = 'localhost', user=user, password = passwd, db=db)
    except mysqldb.Error as e:
        print_error(e.args[1],"connect_db")
    except Exception as err:
        print_error(err,"connect_db")
    return connection

def print_error_import():
	import print_error
	return print_error.print_error
    #print_error_mod = util.spec_from_file_location("print_error",".print_error.py")
    #print_error = util.module_from_spec(print_error_mod)
    #print_error_mod.loader.exec_module(print_error)
    #print_error = print_error.print_error
    #return print_error
