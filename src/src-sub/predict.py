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
        # print(store_data["loss"])
        # print(store_data["mismatches_words"])
        # print(store_data["mismatches"])
    return store_data

# def prepare_test_data(encoded_docs, indexes):
#     shape = encoded_docs.shape
#     with open("test_data.txt","r") as target:
#         data = target.read().split("\n")
#         if data[-1] == "":
#             data = data[:-1]
#         # print(data)
#         test_data = [[0 for i in range(int(shape[1]))] for i in range(2*len(data))]
#         test_data = np.asarray(test_data)
#         print(test_data.shape)
#         y_test_data = [d.split(":")[0] for d in data]
#         x_test_data = [d.split(":")[1] for d in data]
#         print(len(x_test_data))
#         print(len(y_test_data))
#         for key, y in enumerate(y_test_data):
#             test_data[key][indexes[y]] = 1
#         print("\n")
#         for key, x in enumerate(x_test_data):
#             for d in x.split():
#                 test_data[key+int(len(data)/2)][indexes[d]] += 1
#         y_test = np.asarray(test_data[:len(data)])
#         x_test = np.asarray(test_data[len(data):])
#
#         print(x_test)
#         print("\n")
#         print(y_test)
#         print("\n\n")
#         print(encoded_docs[:int(shape[0]/2)])
#         print("\n")
#         print(encoded_docs[int(shape[0]/2):])
#         # for key, doc in enumerate(y_test):
#         #     if encoded_docs[key].any() != y_test[key].any():
#         #         print("failed")
#         # for key, doc in enumerate(x_test):
#         #     if encoded_docs[key + int(shape[0]/2)].any() != x_test[key].any():
#         #         print("failed in x")
#     return

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
    # print(index)
    encoded_docs = t.texts_to_matrix(all_docs, mode='count')
    y = encoded_docs[:size]
    X = encoded_docs[size:]
    return (X, y, index, encoded_docs)

def prepare_test_data2(encoded_docs, index):
    shape = encoded_docs.shape
    with open("test_data.txt", "r") as target:
        data = target.read().split("\n")
    if data[-1] == "":
        data = data[:-1]
    y_test_data = [d.split(":")[0] for d in data]
    x_test_data = [d.split(":")[1] for d in data]
    y_test = [[0 for i in range(int(shape[1]))] for j in range(len(data))]
    x_test = [[0 for i in range(int(shape[1]))] for j in range(len(data))]
    for key,xtd in enumerate(x_test_data):
        for d in xtd.split():
            x_test[key][index[d]] += 1

    for key, ytd in enumerate(y_test_data):
        y_test[key][index[ytd]] = 1

    x_test = np.asarray(x_test, dtype=np.float32)
    y_test = np.asarray(y_test, dtype=np.float32)
    print(len(y_test))
    # print("x_test")
    # print(x_test)
    # print("\n")
    # print("y_test")
    # print(y_test)
    # print("\n\n")
    # print("encoded_docs")
    # print(encoded_docs[:int(shape[0]/2)])
    # print("\n")
    # print(encoded_docs[int(shape[0]/2):])

    return (x_test, y_test)


def one_hot(array):
    temp = []
    return np.argmax(array)

def test(x_test, y_test, index):
    store = read_pkl()
    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(init)

        W1 = tf.convert_to_tensor(store["w1"], dtype = tf.float32)
        W2 = tf.convert_to_tensor(store["w2"], dtype = tf.float32)
        b1 = tf.convert_to_tensor(store["b1"], dtype = tf.float32)
        b2 = tf.convert_to_tensor(store["b2"], dtype = tf.float32)

        W1 = tf.cast(W1, tf.float32)
        for i in range(len(y_test)):
            vec1 = tf.matmul(np.asarray([x_test[i]]), W1)
            vec1 = tf.cast(vec1, tf.float32)
            vec2 = tf.add(vec1, b1)

            vect = tf.add(tf.matmul(vec2, W2), b2)
            vect = sess.run(vect)

            one_hot_y = one_hot(y_test[i])
            one_hot_vect = one_hot(vect[0])

            for key, val in index.items():
                if val == one_hot_y:
                    val_y = key
                    print("y = ", key)
                    print(key)
                if val == one_hot_vect:
                    val_vect = key
                    # print("vector =", key)
                    # print(key)

    return

def main():
    global store
    store = read_pkl()
    total = 500
    df = initialize(total)
    docs = build_matrix(df)
    x, y, index, encoded_docs = tokenize(docs, total)
    # prepare_test_data(encoded_docs, index)
    x_test, y_test = prepare_test_data2(encoded_docs, index)
    test(x_test, y_test, index)

main()
