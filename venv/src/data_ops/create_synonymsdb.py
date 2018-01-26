import pandas as pd
from connect_db import get_engine
from nltk.corpus import wordnet as wn
from print_error import print_error


def save_data():
	engine, meta = get_engine()
	synonym_list = pd.DataFrame(index = None, columns = ['word', 'synonym'])
	word_list = pd.read_sql("words", engine)
	result = word_list.itertuples()

	print("word_list dataset contains {0} words".format(word_list.shape[0]))
	sum = 0
	index = 0
	print("extracting synonyms ...")
	for r in result:
		sum += 1
		for word in wn.synsets(r[1]):
			for syno in word.lemmas():
				if r[1] == word.name().split('.')[0] and len(syno.name()) > 0 and r[1] != syno.name():
					synonym_list.loc[index] = [r[1], syno.name()]
					index += 1
					print(r[1], syno.name())
	
	print("rows matched: {0}".format(index))
	print("traversed {0} words for synonym dataset".format(sum))
	print("removing duplicates ...")
	synonym_list = synonym_list.drop_duplicates(subset='synonym',keep='first', inplace=False)
	print("synonyms dataset contains {0} words".format(synonym_list.shape[0]))	
	"""try:
		synonym_list.to_sql("synonyms", engine, if_exists='append', index=False)
		print("Rows inserted in synonym database: {0}".format(synonym_list.shape[0]))
	except Exception as e:
		print_error(e,"save_data")
	"""
	
def main():
	print("executing create_synonymsdb.py ...")
	save_data()

main()
