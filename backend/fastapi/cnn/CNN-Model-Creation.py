#############
# The complete code (notebook) can be found in the data_exploration directory
# Here is only the abreviated code with less comments and prints
# to comprehend the processing steps
#############
import os
import pickle
import sys

import numpy as np
import pandas as pd
from gensim.models.word2vec import Word2Vec
from keras.layers import (Activation, Conv1D, Dense, Dropout, Embedding,
                          GlobalMaxPool1D, MaxPool1D)
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Dense, Embedding, GlobalMaxPooling1D
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.sequence import pad_sequences
from utils import *

# Add parent dir to system path
sys.path.append('../')


def processing_pipeline(song_data: pd.DataFrame) -> pd.DataFrame:
    """Function executes the entire processing pipeline on given song data.
    Preprocessing steps and idea for the model is used from
    https://www.kaggle.com/code/jagannathrk/word2vec-cnn-text-classification
    Preprocessing steps:

    :param song_data: song data saved in a json file containing song name,
        artist name and lyrics
    :type song_data: pd.DataFrame
    :return: preprocessed song data
    :rtype: pd.DataFrame
    """

    nlp = spacy.load("en_core_web_sm", disable=['ner'])

    for row in range(len(song_data)):
        text_nlp_pipe = list(nlp.pipe([song_data.iloc[row]["Lyric"]]))

        # Tokenization
        song_data.at[row, "Lyric"] = tokenization(text_nlp_pipe)
        # Stop word removal
        song_data.at[row, "Lyric"] = stop_word_removal(
            song_data.iloc[row]["Lyric"])
        # Punctuation removal
        song_data.at[row, "Lyric"] = punctutation_removal(
            song_data.iloc[row]["Lyric"])
        # Lemmatization
        song_data.at[row, "Lyric"] = lemmatization(
            song_data.iloc[row]["Lyric"])
        song_data.at[row, "Lyric"] = " ".join(song_data.iloc[row]["Lyric"])
        song_data.at[row, "Lyric"] = song_data.iloc[row]["Lyric"].lower()
        if row % 500 == 0 and row >= 500:
            print(f"processsed: {row} rows out of {len(song_data)}")
    return song_data


# read in the data of our dataset which has been extended
# with the lastfm labels
df = pd.read_csv('../../../data_exploration/data/song-data-labels-cleaned.csv')
# process data with pipeline
df = processing_pipeline(df)

# merge lyrics together
lyrics = []
for i in df['Lyric']:
    lyrics.append(i.split())

# train the word2vec model
# vector size according to #
# https://moj-analytical-services.github.io/NLP-guidance/NNmodels.html#:~:text=The%20standard%20Word2Vec%20pre%2Dtrained,fewer%20dimensions%20to%20represent%20them.
# mincount = 2 to prevent misspellings
word2vec_model = Word2Vec(lyrics, vector_size=150,
                          window=5, min_count=2, workers=16)

# use the keras tokenizer and apply it to the lyrics
# number in first row is the vocab size from the above print statement
token = Tokenizer(len(word2vec_model.wv))
token.fit_on_texts(df['Lyric'])
text = token.texts_to_sequences(df['Lyric'])
text = pad_sequences(text, 180)

# set the model path dynamically
version = 0
for i in range(1, 100):
    if not os.path.exists('cnn_model_v'+str(i)):
        version = i
        break
model_path = "./cnn_model_v"+str(version)
os.mkdir(model_path)
# save the tokenizer
with open(model_path+'/tokenizer.pickle', 'wb') as handle:
    pickle.dump(token, handle, protocol=pickle.HIGHEST_PROTOCOL)

# encode the labels
le = preprocessing.LabelEncoder()
y = le.fit_transform(df['Mood'])
y = to_categorical(y)
# save the label encoder
np.save(model_path+'/label_encoder.npy', le.classes_)


x_train, x_test, y_train, y_test = train_test_split(
    np.array(text), y, test_size=0.2, stratify=y)


def gensim_to_keras_embedding(model, train_embeddings: bool = False):
    """Function generates a Keras 'Embedding' layer with weights set
    from Word2Vec model's learned word embeddings.
    helper function to use the word2vec as an layer in keras
    taken from the gensim wikipage:
    https://github.com/RaRe-Technologies/gensim/wiki/Using-Gensim-Embeddings-with-Keras-and-Tensorflow

    :param model: Word2Vec Embedding model
    :type model: gensim.model
    :param train_embeddings: If False, the returned weights are frozen
        and stopped from being updated. If True, the weights can / will
        be further updated in Keras, defaults to False
    :type train_embeddings: bool, optional
    :return: Embedding layer, to be used as input to deeper network layers.
    :rtype: `keras.layers.Embedding`
    """

    keyed_vectors = model.wv  # structure holding the result of training
    weights = keyed_vectors.vectors  # vectors themselves, a 2D numpy array
    # which row in `weights` corresponds to which word?
    index_to_key = keyed_vectors.index_to_key

    layer = Embedding(
        input_dim=weights.shape[0],
        output_dim=weights.shape[1],
        weights=[weights],
        trainable=train_embeddings,
    )
    return layer


# Defining the model
keras_model = Sequential()
keras_model.add(gensim_to_keras_embedding(word2vec_model, True))
keras_model.add(Dropout(0.2))
keras_model.add(Conv1D(50, 5, activation='relu', padding='same', strides=1))
keras_model.add(Conv1D(50, 5, activation='relu', padding='same', strides=1))
keras_model.add(MaxPool1D())
keras_model.add(Dropout(0.2))
keras_model.add(Conv1D(100, 5, activation='relu', padding='same', strides=1))
keras_model.add(Conv1D(100, 5, activation='relu', padding='same', strides=1))
keras_model.add(MaxPool1D())
keras_model.add(Dropout(0.2))
keras_model.add(Conv1D(150, 5, activation='relu', padding='same', strides=1))
keras_model.add(Conv1D(150, 5, activation='relu', padding='same', strides=1))
keras_model.add(GlobalMaxPool1D())
keras_model.add(Dropout(0.2))
keras_model.add(Dense(200))
keras_model.add(Activation('relu'))
keras_model.add(Dropout(0.2))
# Number of moods to be classified to
keras_model.add(Dense(17))
keras_model.add(Activation('softmax'))
keras_model.compile(loss='binary_crossentropy',
                    metrics=['acc'], optimizer='adam')

keras_model.fit(x_train, y_train, batch_size=32, epochs=3,
                validation_data=(x_test, y_test))

# save keras model
keras_model.save(model_path)
