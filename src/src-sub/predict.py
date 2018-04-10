import tensorflow as tf
import keras
import numpy as np
import pandas as pd
from keras.preprocessing.text import Tokenizer
import pickle
import pprint

store = {}

def read_pkl():
    with open("store.pickle", "rb") as pkl_r:
        store_data = pickle.load(pkl_r)
        print(store_data["loss"])
        # print(store_data["mismatches_words"])
        print(store_data["mismatches"])
    return store_data

def prepare_test_data(encoded_docs, indexes):
    shape = encoded_docs.shape
    with open("test_data.txt","r") as target:
        data = target.read().split("\n")
        if data[-1] == "":
            data = data[:-1]
        # print(data)
        test_data = [[0 for i in range(int(shape[1]))] for i in range(2*len(data))]
        test_data = np.asarray(test_data)
        print(test_data.shape)
        y_test_data = [d.split(":")[0] for d in data]
        x_test_data = [d.split(":")[1] for d in data]
        print(len(x_test_data))
        print(len(y_test_data))
        for key, y in enumerate(y_test_data):
            test_data[key][indexes[y]] = 1
        print("\n")
        for key, x in enumerate(x_test_data):
            for d in x.split():
                test_data[key+int(len(data)/2)][indexes[d]] += 1
        y_test = np.asarray(test_data[:len(data)])
        x_test = np.asarray(test_data[len(data):])

        print(x_test)
        print("\n")
        print(y_test)
        print("\n\n")
        print(encoded_docs[:int(shape[0]/2)])
        print("\n")
        print(encoded_docs[int(shape[0]/2):])
        # for key, doc in enumerate(y_test):
        #     if encoded_docs[key].any() != y_test[key].any():
        #         print("failed")
        # for key, doc in enumerate(x_test):
        #     if encoded_docs[key + int(shape[0]/2)].any() != x_test[key].any():
        #         print("failed in x")
    return

def initialize(size=10):
    df = pd.read_csv("db/final_final_final.csv", names=["word","definition"], sep=":", index_col=None, keep_default_na=False, na_values=[""])
    df = df[:size]
    df = df.values.tolist()
    df = [[f[0], f[1].strip()] for f in df]
    return df

def build_matrix(df):
    all_docs = []
    words = [arr[0] for arr in df]
    sents = [arr[1] for arr in df]
    all_docs = words + sents
    return all_docs

def tokenize(all_docs, size):
    t = Tokenizer()
    t.fit_on_texts(all_docs)
    index = t.word_index
    print(index)
    encoded_docs = t.texts_to_matrix(all_docs, mode='count')
    y = encoded_docs[:size]
    X = encoded_docs[size:]
    return (X, y, index, encoded_docs)

def main():
    global store
    store = read_pkl()
    total = 10
    df = initialize(total)
    docs = build_matrix(df)
    x, y, index, encoded_docs = tokenize(docs, total)
    prepare_test_data(encoded_docs, index)

main()
