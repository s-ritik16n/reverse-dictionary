import pandas as pd
from connect_db import get_engine
from print_error import print_error

engine, meta = get_engine()
definitions = pd.read_sql("definitions", engine)

def stem():
    pass

def remove_stopwords():
    pass
    
definitions['definition'] = definitions.apply()   # tem
definitions['definition'] = definitions.apply()   # remove stepwords
