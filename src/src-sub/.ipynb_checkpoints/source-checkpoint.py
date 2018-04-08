import keras
import pandas as pd
import numpy as np
from keras import losses
from keras.layers import Dense
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
size = 10
df = pd.read_csv("db/final_final.csv", names=["word","definition"], sep=":", index_col=None, keep_default_na=False, na_values=[""])
df = df[:size]
df = df.values.tolist()
print(df)
all_docs = []
words = [arr[0] for arr in df]
print(words)
sents = [arr[1] for arr in df]
print(sents)
all_docs = words + sents
print(all_docs)
t = Tokenizer()
t.fit_on_texts(all_docs)
# print(t.word_counts)
# print(t.document_count)
print(t.word_index)
# print(t.word_docs)
encoded_docs = t.texts_to_matrix(all_docs, mode='count')
print("\n")
print(encoded_docs)
X = encoded_docs[:size]
y = encoded_docs[size:]
print(X)
print("\n")
print(y)
model = Sequential()
model.add(Dense(3,activation='sigmoid', input_dim=encoded_docs.shape[1]))
model.add(Dense(size, activation='sigmoid'))
model.compile(optimizer=keras.optimizers.SGD(lr=0.01), loss='mse')
model.summary()
model.fit(X, y, epochs=1000, verbose=1)