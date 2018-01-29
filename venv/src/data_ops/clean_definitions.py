import pandas as pd
from connect_db import get_engine
from print_error import print_error
from nltk.corpus import stopwords

stopwords = stopwords.words('english')
engine, meta = get_engine()
definitions = pd.read_sql("definitions", engine)

def stem(definition):
	pass    

def remove_stopwords(definition):
    return ' '.join([d for d in definition.split() if d not in stopwords])
    
#definitions['definition'] = definitions['definition'].apply(stem)   # stem
definitions['definition'] = definitions['definition'].apply(remove_stopwords)   # remove stepwords
definitions.to_sql("definitions_new", engine,if_exists='append', index=False)
