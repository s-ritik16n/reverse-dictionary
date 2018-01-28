import pandas as pd
from connect_db import get_engine
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import threading as mt
import gc

if(gc.isenabled()):
	gc.disable()

stopwords = stopwords.words("english")
engine, meta = get_engine()

words_df = pd.read_sql_table("words", engine)
hypernyms_df = pd.read_sql_table("hypernyms", engine)
hyponyms_df = pd.read_sql_table("hyponyms", engine)
synonyms_df = pd.read_sql_table("synonyms", engine)

def get_definitions(word):
	definition_list = []
	syns = wn.synsets(word)
	for s in syns:
		for definition in s.definition().split(";"):
			definition_list.append([word, ' '.join([d for d in definition.split() if d not in stopwords])])
	return definition_list
		
def get_definitions_from_df(df):
	words = df.itertuples()
	definitions = []
	df = pd.DataFrame(index=None, columns = ['word','definitions'])
	for word in words:
		word = word[1]
		df.append()
	return definitions
	
def insert_definitions(word, df):
	df_list = df.loc[df['word'] == word]
	df_list.columns=['word', 'definition']
	df_list = pd.unique(pd.Seris(df_list['word']))
	 = get_definitions_from_df(df_list)
	df_temp = pd.DataFrame(get_definitions(word), index = None,columns = ['word','definition'])
	df_temp.to_sql("definitions", engine, if_exists = 'append', index=False)

def main():
	words = words_df.itertuples()
	for word in words:
		word = word[1]
		definitions_list = get_definitions(word, None)
		definitions_df = pd.DataFrame(definitions_list, index=None, columns = ['word','definition'])
		definitions_df.to_sql("definitions", engine, if_exists = 'append', index=False)
		mt.Thread(target=insert_definitions, args = (word, hypernyms_df,)).start()
		mt.Thread(target=insert_definitions, args = (word, hyponyms_df,)).start()
		mt.Thread(target=insert_definitions, args = (word, synonyms_df,)).start()

main()
