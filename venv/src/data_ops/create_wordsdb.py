import pandas as pd

from sqlalchemy import TEXT, create_engine, MetaData
from nltk.corpus import words
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from connect_db import connect_db as cb
from print_error import print_error
from config import db_info

st = SnowballStemmer(language="english")
engine = create_engine("mysql+mysqldb://root:"+'2340532'+"@localhost/wordnetdb")
meta = MetaData(bind = engine)


def stem(word):
	return st.stem(word)

def load_data():
	print("loading nltk words in dataframe ...")
	return pd.DataFrame(words.words(), index = None,columns = ['word'])

def clean_data(word_list):
	print("stemming words ...")
	word_list['word'] = word_list.applymap(stem)
	print("removing stopwords ...")
	word_list = word_list[~word_list['word'].isin(stopwords.words('english'))]
	print("word list contains {0} words".format(word_list.shape[0]))
	print("dropping duplicates ...")
	word_list = word_list.drop_duplicates(subset='word', keep='first',inplace = False)
	print("word list contains {0} words after removing duplicates".format(word_list.shape[0]))
	return word_list

def save_data(word_list):
	print("inserting data ...")
	word_list.to_sql("words", engine,if_exists = 'append', index = False,dtype=TEXT)
	print("data saved in table 'words' in  wordnetdb ...")
	return

def main():
	word_list = clean_data(load_data())
	try:
		save_data(word_list)
	except Exception as e:
		print_error(e, "save_data")
	return

main()
