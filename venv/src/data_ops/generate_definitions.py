from connect_db import get_engine
import pandas as pd
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords

engine, meta = get_engine()

words_list = pd.read_sql_table("words", engine)
hypernyms_list = pd.read_sql_table("hypernyms", engine)
hyponyms_list = pd.read_sql_table("hyponyms", engine)
synonyms_list = pd.read_sql_table("synonyms", engine)
definitions_list = pd.DataFrame(index=None,columns=['word','definition'])

index = 0
words = words_list.itertuples()

def get_definitions(word):
	definition_list = []
	word_synsets = wn.synsets(word)
	for syns in word_synsets:
		definitions = syns.definition().split(";")
		for definition in definitions:
			definition_list.append(' '.join([d for d in definition.split() if d not in stopwords.words('english')]))
	return definition_list

def insert_definitions(definitions, word):
	global index
	for d in definitions:
		definitions_list.loc[index] = [word, d]
		index += 1
	return

def main():
	print("executing generate_definitons.py ...")
	print("executing main ...")
	print("extracting definitions and saving to dataframe ...")
	for word in words:
		print(index)
		definitions = get_definitions(word[1])
		insert_definitions(definitions, word[1])
		hypernyms = hypernyms_list.loc[hypernyms_list['word'] == word[1]]
		hypernyms = hypernyms.itertuples()
		for hyper in hypernyms:
			definitions = get_definitions(hyper[1])
			insert_definitions(definitions, word[1])
		hyponyms = hyponyms_list.loc[hyponyms_list['word'] == word[1]]
		for hypo in hyponyms:
			definitions = get_definitions(hypo[1])
			insert_definitions(definitions, word[1])
		synonyms = synonyms_list.loc[synonyms_list['word'] == word[1]]
		for syn in synonyms:
			definitions = get_definitions(syn[1])
			insert_definitions(definitions, word[1])
	print("definitons dataset contains {0} entries".format(definitions.shape[0]))
	try:
		definitions_list.to_sql("definitions", engine, if_exists='append')
	except Exception as e:
		print_error(e,"in function main -- generate_definitions.py")

main()
