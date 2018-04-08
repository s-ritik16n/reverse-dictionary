"""
extracting hypernyms from wordnet in nltk and saving to wordnetdb database
"""

import pandas as pd
from connect_db import get_engine
from nltk.corpus import wordnet as wn
from sqlalchemy import TEXT
from print_error import print_error


def save_data():
	engine, meta = get_engine()
	hypernym_list = pd.DataFrame(index = None, columns = ['word', 'hypernym'])
	word_list = pd.read_sql("words", engine)
	result = word_list.itertuples()

	print("word_list dataset contains {0} words".format(word_list.shape[0]))
	sum = 0
	index = 0
	for r in result:
		sum += 1
		for word in wn.synsets(r[1]):
			for hyper in word.hypernyms():
				if r[1] == word.name().split('.')[0] and len(hyper.name()) > 0:
					hypernym_list.loc[index] = [r[1], hyper.name().split('.')[0]]
					index += 1
	
	print("rows matched: {0}".format(index))
	print("traversed {0} words for hypernym dataset".format(sum))
	
	try:
		hypernym_list.to_sql("hypernyms", engine, if_exists='append', index=False, dtype=TEXT)
	except Exception as e:
		print_error(e,"save_data")
	
	print("Rows inserted in hypernym database: {0}".format(hypernym_list.shape[0]))
	
def main():
	print("executing create_hypernyms.py ...")
	save_data()

main()
