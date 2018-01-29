import pandas as pd
from connect_db import get_engine
from print_error import print_error
from nltk.corpus import stopwords

stopwords = stopwords.words('english')
engine, meta = get_engine()
definitions = pd.read_sql("definitions", engine)
words = []

def stem(definition):
	pass    

def remove_stopwords(definition):
    return ' '.join([d for d in definition.split() if d not in stopwords])

def stop_words_main():
	#definitions['definition'] = definitions['definition'].apply(stem)   # stem
	definitions['definition'] = definitions['definition'].apply(remove_stopwords)   # remove stepwords
	definitions.to_sql("definitions_new", engine,if_exists='append', index=False)

def get_non_matching_words(definition):
	words.extend(d for d in definition.split() if d not in definitions['word'] and d not in words)

def common_words_main():
	definitions['definition'].apply(get_non_matching_words)

common_words_main()
print(len(words))
