import tensorflow as tf
import keras
import numpy as np
import pandas as pd
from keras.preprocessing.text import Tokenizer

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
    encoded_docs = t.texts_to_matrix(all_docs, mode='count')
    y = encoded_docs[:size]
    X = encoded_docs[size:]
    return (X, y, index, encoded_docs)

def one_hot(array):
    temp = []
    return np.argmax(array)

def tensor(x_train, y_train, indexes, encoded_docs):
    x_train = np.asarray(x_train)
    y_train = np.asarray(y_train)
    print(x_train.shape)
    print(y_train.shape)
    print(encoded_docs)
    size = x_train.shape[0]
    input_layer_neurons = size
    columns = x_train.shape[1]
    vocab_size = columns

    x = tf.placeholder(tf.float32, shape=(size, columns))
    y_label = tf.placeholder(tf.float32, shape=(size, columns))

    EMBEDDING_DIM = 3
    W1 = tf.Variable(tf.random_normal([columns, EMBEDDING_DIM]))
    b1 = tf.Variable(tf.random_normal([EMBEDDING_DIM]))
    hidden_repr = tf.add(tf.matmul(x, W1), b1)

    W2 = tf.Variable(tf.random_normal([EMBEDDING_DIM, columns]))
    b2 = tf.Variable(tf.random_normal([columns]))

    prediction = tf.nn.softmax(tf.add(tf.matmul(hidden_repr, W2), b2))

    sess = tf.Session()
    init = tf.global_variables_initializer()


    cross_entropy_loss = tf.reduce_mean(-tf.reduce_sum(y_label * tf.log(prediction+1e-8), reduction_indices=[1]))
    # train_step = tf.train.AdamOptimizer(0.1)
    # train_step = train_step.minimize(cross_entropy_loss)

    train_step = tf.train.GradientDescentOptimizer(0.05).minimize(cross_entropy_loss)
    sess.run(init)
    # sess.run(sess.graph.get_tensor_by_name('beta1_power/Assign:0'))
    # sess.run(sess.graph.get_tensor_by_name('beta2_power/Assign:0'))
    n_iters = 10000


    for _ in range(n_iters):
        print(_)
        sess.run(train_step, feed_dict = {x: x_train, y_label: y_train})
        loss = sess.run(cross_entropy_loss, feed_dict = {x: x_train, y_label: y_train})
        if loss == np.nan:
            break
        print('loss is: ', loss)

    # vectors = sess.run(W1+b1)
    W1 = tf.cast(W1, tf.float64)
    mismatches = 0
    mismatches_words = []
    print(indexes)
    for i in range(len(y_train)):
        vec1 = tf.matmul(np.asarray([x_train[i]]), W1)
        # tf.cast(vec1, tf.float32)
        vec1 = tf.cast(vec1, tf.float32)
        vec2 = tf.add(vec1,b1)

        vect = tf.add(tf.matmul(vec2,W2), b2)
        vect = sess.run(vect)

        print(y_train[i])
        print(vect[0])
        one_hot_y = one_hot(y_train[i])
        one_hot_vect = one_hot(vect[0])
        print(one_hot_y)
        print(one_hot_vect)
        for key, val in indexes.items():
            if val == one_hot_y:
                val_y = key
                print("y=", key)
            if val == one_hot_vect:
                val_vect = key
                print("vector=", key)

        if val_y != val_vect:
            mismatches += 1
            mismatches_words.append((val_y, val_vect))
        print("\n")
    print("total number of mismatches = ", str(mismatches))
    print(mismatches_words)
    return

def compute(y,output, size):

    print("\none_hot for actual outcome - ")
    output_one_hot = one_hot(output)
    print(output_one_hot)

    count = 0
    for key, val in enumerate(output_one_hot):
        if y[key][val] != 1:
            count += 1

    print("\ntotal number of mismatches = {}".format(str(count)))
    print("training data accuracy = {0}{1}".format(str((size-count)*100/size), "%"))

def main():
    total = 100
    df = initialize(total)
    docs = build_matrix(df)
    x, y, index, encoded_docs = tokenize(docs, total)
    tensor(x, y, index, encoded_docs)
    return
main()
