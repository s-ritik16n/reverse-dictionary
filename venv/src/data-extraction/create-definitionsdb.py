"""
extracting definitions from wordnet in nltk and saving to wordnetdb database
"""
import pandas as pd
from nltk.corpus import wordnet as wn
from connect_db import get_engine
from print_error import print_error
from nltk.corpus import stopwords

engine, meta = get_engine()
st = stopwords.words('english')

df = pd.DataFrame(index=None, columns = ['word','definition'])
index = 0
for word in wn.all_synsets():
	word_text = word.name().split('.')[0]
	df = df.append({'word':word_text,'definition': word.definition()}, ignore_index=True)
	index += 1
	print(index)

df.to_sql("definitions", engine, if_exists='append', index=False)
