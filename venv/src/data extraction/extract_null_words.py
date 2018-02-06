"""
extract words whose definition is not present in defiitions.csv
"""

import pandas as pd

df = pd.read_csv("db/definitions.csv", names=["word","definition"], sep=":")
words = pd.DataFrame(columns = ["word","definition"], index=None)

def extract_null_words(word):
	if df.loc[df["word"] == word]["definition"] is None:
		words.append({"word":word}, ignore_index=True)

#df["word"].apply(extract_null_words)
words = pd.isnull(df["definition"])

indices = []
for i in range(len(words)):
	if words[i] == True:
		print(i)
		indices.append(i)

#print(df.info())
#print(len(indices))

new_df = df[df["word"] is None]
print(new_df.info())
new_df1 = df[df["definition"] is None]
print(new_df1.info())
