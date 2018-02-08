"""
extracting antonyms from from wordnet utility in nltk and saving to database
"""

import pandas as pd
from connect_db import get_engine
from nltk.corpus import wordnet as wn
from print_error import print_error


def save_data():
	engine, meta = get_engine()
	antonym_list = pd.DataFrame(index = None, columns = ['word', 'antonym'])
	word_list = pd.read_sql("words", engine)
	result = word_list.itertuples()

	print("word_list dataset contains {0} words".format(word_list.shape[0]))
	sum = 0
	index = 0
	for r in result:
		sum += 1
		for word in wn.synsets(r[1]):
			for anto in word.lemmas():
				if r[1] == word.name().split('.')[0] and anto.antonyms():
					antonym_list.loc[index] = [r[1], anto.antonyms()[0].name()]
					index += 1
	
	print("rows matched: {0}".format(index))
	print("traversed {0} words for antonym dataset".format(sum))
	
	try:
		antonym_list.to_sql("antonyms", engine, if_exists='append', index=False)
		print("Rows inserted in antonyms database: {0}".format(antonym_list.shape[0]))
	except Exception as e:
		print_error(e,"save_data")
	
def main():
	print("executing create_antonymsdb.py ...")
	save_data()

main()
