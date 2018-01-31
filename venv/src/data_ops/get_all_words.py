# extract all words and save to database

import pandas as pd
from connect_db import get_engine
from print_error import print_error
import sys

engine, meta = get_engine()

#all data frames
words_df = pd.read_sql("words", engine)['word'].unique()
hyper_df = pd.read_sql("hypernyms",engine)['word'].unique()
hypo_df = pd.read_sql("hyponyms", engine)['word'].unique()
syno_df = pd.read_sql("synonyms", engine)['word'].unique()
def_df = pd.read_sql("definintons",engine)['word'].unique()

def write_info(df):
    print("*"*10)
    print("all_words")
    print(all_words.info())
    #print("all_words dataset contains {0} words".foramt(df.count(axis=1)))
    

def get_all_words():
    # merge all dataframes
    all_words_df = pd.DataFrame(columns = ['word'], index=None)
    all_words = all_words.append(words_df, ignore_index=True)
    all_words = all_words.append(hyper_df, ignore_index=True)
    all_words = all_words.append(hypo_df, ignore_index=True)
    all_words = all_words.append(syno_df, ignore_index=True)
    
    # drop duplicates from the dataframe
    all_words = all_words.drop_duplicates(subset=['word'], keep='first', inplace=False)
    
    # display dataframe information
    write_info(all_words)
    
    #write to database
    try:
        all_words.to_sql("all_words", engine, if_exists='append', index=False)
    except Exception as e:
        print_error(e,"get_all_words")
        sys.exit(1)
        
