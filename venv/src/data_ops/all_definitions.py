import pandas as pd
import requests as req
from connect_db import get_engine
from print_error import print_error

engine, meta = get_engine()
words_df = pd.read_sql("all_words", engine, columns=['word'])
def_df = pd.DataFrame(columns = ['word','definition'], index=None)
no_definitions = []

def get_definition(word):
	params={"format":"json"}
	global def_df
	r = req.get("https://owlbot.info/api/v2/dictionary/"+word, params=params).json()
	print(word)
	print(r)
	if len(r)==0:
		no_definitions.append(word)
		return
	for obj in r:
		def_df = def_df.append({"word":word,"definition":obj["definition"]}, ignore_index=True)
	return

def main():
	words_df['word'].apply(get_definition)
	print("definitions found: {0}".format(def_df.count(axis=1)))
	print("definitions not found: {0}".format(len(no_definitions)))
	try:
		def_df.to_sql("all_definitions",engine, if_exists='replace', index=False)
		nodef_df = pd.DataFrame(no_definitions, columns=['word'], index=None)
		nodef_df.to_sql("no_definitions", engine, if_exists='replace', index=False)
	except Exception as e:
		print_error(e,"main")

main()
