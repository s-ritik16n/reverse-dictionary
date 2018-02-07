"""
extract words whose definition is not present in defiitions.csv
"""

import pandas as pd
import numpy as np

df = pd.read_csv("db/definitions.csv", names=["word","definition"], sep=":", index_col=None, keep_default_na=False, na_values=[""])
words = pd.DataFrame(columns=["word"], index=None)

indices = []
def null(word):
	if str(word) == 'nan':
		indices.append(word)

ww = pd.isnull(df['word'])
null_word_indices = []
for id,w in enumerate(ww):
	if w is True:
		null_word_indices.append(id)
		# print(df.loc[id][0], df.loc[id][1])

dd = pd.isnull(df['definition'])
null_def_indices = []
for id,d in enumerate(dd):
	if d is True:
		null_def_indices.append(id)
		# print(df.loc[id][0], df.loc[id][1])

for el in null_word_indices:
	if el in null_def_indices:
		null_def_indices.remove(el)

print("df info before deletion")
print(df.info())
print("*"*10)

df = df.drop(null_word_indices, inplace=False)
df = df.drop(null_def_indices, inplace=False)
df = df.reset_index(drop=True)
print(df.info())

df.to_csv("db/definitions.csv", sep=":", columns=["word","definition"], header=False, index=False, mode="w")
