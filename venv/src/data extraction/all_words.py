# extract all words and save to database

import pandas as pd
from connect_db import get_engine
from print_error import print_error
import sys

engine, meta = get_engine()

#all data frames
words_df = pd.read_sql("words", engine, columns=['word'])
hyper_df = pd.read_sql("hypernyms",engine, columns = ['word'])
hypo_df = pd.read_sql("hyponyms", engine, columns = ['word'])
syno_df = pd.read_sql("synonyms", engine, columns = ['word'])
def_df = pd.read_sql("definitions",engine, columns = ['word'])

def write_info(df):
	print("*"*10)
	print("all_words")
	print(df.count())
	print(df.info())

def main():
	# create dataframe to contain all words
	all_words_df = pd.DataFrame(columns = ['word'], index=None)
	
	#merge all dataframes
	all_words_df = all_words_df.append(words_df, ignore_index=True)
	all_words_df = all_words_df.append(hyper_df, ignore_index=True)
	all_words_df = all_words_df.append(hypo_df, ignore_index=True)
	all_words_df = all_words_df.append(syno_df, ignore_index=True)
	all_words_df = all_words_df.append(def_df, ignore_index=True)
 
	# drop duplicates from the dataframe
	all_words_df = all_words_df.drop_duplicates(subset=['word'], keep='first', inplace=False)
    
	# display dataframe information
	write_info(all_words_df)
	#write to database
	try:
		all_words_df.to_csv("words.csv",index=False)
	except Exception as e:
		print_error(e,"get_all_words")
		sys.exit((1))

main()        
