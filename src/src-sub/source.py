import keras
import pandas as pd
import numpy as np
from keras import losses
from keras.layers import Dense
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
import os
import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
size = 10
df = pd.read_csv("db/final_final.csv", names=["word","definition"], sep=":", index_col=None, keep_default_na=False, na_values=[""])
df = df[:size]
df = df.values.tolist()
print(df)
all_docs = []
words = [arr[0] for arr in df]
# print(words)
sents = [arr[1] for arr in df]
# print(sents)
all_docs = words + sents
# print(all_docs)
t = Tokenizer()
t.fit_on_texts(all_docs)
# print(t.word_counts)
# print(t.document_count)
print(t.word_index)
# print(t.word_docs)
encoded_docs = t.texts_to_matrix(all_docs, mode='count')
print("\n")
# print(encoded_docs)
y = encoded_docs[:size]
X = encoded_docs[size:]
print("X = ")
print(X)
print("\n")
print("y = ")
print(y)
# model = Sequential()
# model.add(Dense(3,activation='sigmoid', input_dim=encoded_docs.shape[1]))
# model.add(Dense(encoded_docs.shape[1], activation='sigmoid'))
# model.compile(optimizer=keras.optimizers.SGD(lr=0.2), loss='mse')
# model.summary()
# model.fit(X, y, epochs=100, verbose=1)

def sigmoid(x):
    return np.around(1/(1+np.exp(-x)), decimals=30)

def der_sigmoid(x):
    return 1*(1-x)

epoch=200000
lr=0.1

input_layer_neurons = encoded_docs.shape[1] # 3
hiddenlayer_neurons = 3
output_neurons = encoded_docs.shape[1]

wh = np.random.uniform(size = (input_layer_neurons, hiddenlayer_neurons))
bh = np.random.uniform(size = (1, hiddenlayer_neurons))
wout = np.random.uniform(size = (hiddenlayer_neurons, output_neurons))
bout = np.random.uniform(size = (1, output_neurons))

for i in range(epoch):

    # print("epoch - {}".format(str(i)))
    # Forward propagation
    hidden_layer_input1 = np.dot(X,wh)
    hidden_layer_input = hidden_layer_input1 + bh
    hidden_layer_activations = sigmoid(hidden_layer_input)
    output_layer_input1 = np.dot(hidden_layer_activations, wout)
    output_layer_input = output_layer_input1 + bout
    output = sigmoid(output_layer_input)

    # Backpropagation
    E = y-output
    slope_output_layer = der_sigmoid(output)
    slope_hidden_layer = der_sigmoid(hidden_layer_activations)
    d_output = E * slope_output_layer
    Error_at_hidden_layer = d_output.dot(wout.T)
    d_hiddenlayer = Error_at_hidden_layer * slope_hidden_layer
    wout += hidden_layer_activations.T.dot(d_output) * lr
    bout += np.sum(d_output, axis=0, keepdims = True) * lr
    wh += X.T.dot(d_hiddenlayer) * lr
    bh += np.sum(d_hiddenlayer, axis=0, keepdims = True) * lr

print(output)
