"""
extract words whose definition is not present in defiitions.csv
"""

import pandas as pd
import numpy as np

df = pd.read_csv("db/definitions.csv", names=["word","definition"], sep=":", index_col=None)
words = pd.DataFrame(columns=["word"], index=None)

indices = []
def null(word):
	if str(word) == 'nan':
		indices.append(word)

ww = pd.isnull(df['word'])
for id,w in enumerate(ww):
	if w is True:
		print(df.loc[id][0], df.loc[id][1])

print("*"*10)

dd = pd.isnull(df['definition'])
for id,d in enumerate(dd):
	if d is True:
		print(df.loc[id][0], df.loc[id][1])
