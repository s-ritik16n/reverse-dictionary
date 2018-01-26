from connect_db import get_engine
import pandas as pd

engine, meta = get_engine

words_list = pd.read_sql_table("words", engine)
hypernyms_list = pd.read_sql_table("hypernyms", engine)
hyponyms_list = pd.read_sql_table("hyponyms", engine)
synonyms_list = pd.read_sql_table("synonyms", engine)

definitions_list = pd.DataFrame(index=None,columns=['word','definition'])

words = words_list.itertuples()

for word in words:
	hypernyms = hypernyms_list['hypernym'][hypernyms_list.loc[hypernyms_list['word'] == word]]]	
	hyponyms = hyponyms_list
