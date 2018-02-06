"""
remove stopwords and other trivial content from definitions.csv
"""

import pandas as pd
from connect_db import get_engine
from print_error import print_error
from nltk.corpus import stopwords

stopwords = stopwords.words("english")

engine, meta = get_engine()
df = pd.read_csv("db/definitions.csv", sep=":", names = ["word","definition"])
words = pd.DataFrame(columns = ["word"], index = None)

print(df.info())

def remove_stopwords(definition):
	return ' '.join([d for d in definition.split() if d not in stopwords])

def more_words(definition):
	word = [d for d in definition.split() if not any(df["word"] == word)]
	for w in word:
		words.append({"word":w}, ignore_index=True)

def main():
	global df
	df = df.dropna(axis=1, how='any')
	print("*"*5)
	print(df.count())
	df.to_csv("db/definitions.csv", sep=":", columns=["word","definitions"], mode="w")
	#df['definition'] = df['definition'].apply(remove_stopwords)
	#print("*"*5)
	#print(df.info())
	#df.to_csv("db/definitions.csv", sep = ":", names=["word","definition"], mode="w")
	#df['definition'].apply(more_words)
	#words.to_csv("db/remaining_words.csv", names = ["word"], mode="w")

main()
