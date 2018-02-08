"""
remove non-alphanumeric characters form rows
"""

import pandas as pd

df = pd.read_csv("db/definitions.csv", sep=":", index_col=None, names=["word","definition"])
final_df = pd.DataFrame(columns = ["word","definition"], index=None)

print(df.info())

symbols = [":",",",")","("]

def treat_symbols(word):
    global final_df
    definition = str(df.loc[df["word"] == word]["definition"])
    definition = "".join(d for d in list(definition) if d not in symbols)
    # print(definition)
    if ";" in definition:
        definitions = [d for d in definition.split(";")]
        for d in definitions:
            final_df = final_df.append({"word":word,"definition":d},ignore_index=True)

df['word'].apply(treat_symbols)
print(final_df.info())
