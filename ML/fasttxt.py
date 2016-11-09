'''Trains a LSTM on the IMDB sentiment classification task.
The dataset is actually too small for LSTM to be of any advantage
compared to simpler, much faster methods such as TF-IDF + LogReg.
Notes:
- RNNs are tricky. Choice of batch size is important,
choice of loss and optimizer is critical, etc.
Some configurations won't converge.
- LSTM loss decrease patterns during training can be quite different
from what you see with CNNs/MLPs/etc.
'''
# from keras.utils.visualize_util import plot

import numpy as np
np.random.seed(1337)  # for reproducibility
from tensorflow.contrib import learn

from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding
from keras.layers import LSTM, SimpleRNN, GRU
from keras import callbacks
import json
import mypath as path
import random
import pandas
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Embedding
from keras.layers import GlobalAveragePooling1D
from keras.datasets import imdb

def create_ngram_set(input_list, ngram_value=2):
    """
    Extract a set of n-grams from a list of integers.
    >>> create_ngram_set([1, 4, 9, 4, 1, 4], ngram_value=2)
    {(4, 9), (4, 1), (1, 4), (9, 4)}
    >>> create_ngram_set([1, 4, 9, 4, 1, 4], ngram_value=3)
    [(1, 4, 9), (4, 9, 4), (9, 4, 1), (4, 1, 4)]
    """
    return set(zip(*[input_list[i:] for i in range(ngram_value)]))


def add_ngram(sequences, token_indice, ngram_range=2):
    """
    Augment the input list of list (sequences) by appending n-grams values.
    Example: adding bi-gram
    >>> sequences = [[1, 3, 4, 5], [1, 3, 7, 9, 2]]
    >>> token_indice = {(1, 3): 1337, (9, 2): 42, (4, 5): 2017}
    >>> add_ngram(sequences, token_indice, ngram_range=2)
    [[1, 3, 4, 5, 1337, 2017], [1, 3, 7, 9, 2, 1337, 42]]
    Example: adding tri-gram
    >>> sequences = [[1, 3, 4, 5], [1, 3, 7, 9, 2]]
    >>> token_indice = {(1, 3): 1337, (9, 2): 42, (4, 5): 2017, (7, 9, 2): 2018}
    >>> add_ngram(sequences, token_indice, ngram_range=3)
    [[1, 3, 4, 5, 1337], [1, 3, 7, 9, 2, 1337, 2018]]
    """
    new_sequences = []
    for input_list in sequences:
        new_list = input_list[:]
        new_list=new_list.tolist()

        for i in range(len(new_list)-ngram_range+1):
            for ngram_value in range(2, ngram_range+1):
                ngram = tuple(new_list[i:i+ngram_value])
                if ngram in token_indice:
                    new_list.append(token_indice[ngram])
        new_sequences.append(new_list)

    return new_sequences

MAX_DOCUMENT_LENGTH = 140

correctword=0
totleword=0
global n_words
# Prepare training and testing data
times=10
indeslixt=[]
with open(path.Featurepath+'indexshuffled.txt',encoding='utf-8',mode='r') as writer:
    indeslixt=json.loads(writer.read())
listofrumor=[]
listofnews=[]
lenofpiece=int(len(indeslixt)/times+0.5)

with open(path.Featurepath+'featuresrumorsTextlable.txt', mode='r') as writer:
    for line in writer:
        JSON=json.loads(line)
        listofrumor.append(JSON)

with open(path.Featurepath+'featuresNewsTextlable.txt', mode='r') as writer:
    for line in writer:
        JSON=json.loads(line)
        listofnews.append(JSON)
tweetresult={}

choice=200
recall=0
for time in range(times):
    if time >3:
        continue
    listofPara=list()
    listofresult=list()

    listofParatest=list()
    listofresulttest=list()
    tweetIDtest=[]

    for rumor in listofrumor:
            if random.randint(1, 100)>choice:
                continue
            if rumor['eventID'] not in  indeslixt[time*lenofpiece: time*lenofpiece+lenofpiece]:
                for rumortext in rumor['data']:
                    rumortextstr=rumortext['features']
                    listofPara.append(rumortextstr)
                    listofresult.append(1)
            else:
                print(rumor['eventID'])
                for rumortext in rumor['data']:
                    rumortextstr=rumortext['features']
                    tweetIDtest.append(rumortext['tweetid'])
                    listofParatest.append(rumortextstr)
                    listofresulttest.append(1)
    for news in listofnews:
            if random.randint(1, 100)>choice:
                continue
            if news['eventID'] not in  indeslixt:
                continue
            if news['eventID'] not in  indeslixt[time*lenofpiece: time*lenofpiece+lenofpiece]:
                for rumortext in news['data']:
                    rumortextstr=rumortext['features']

                    listofPara.append(rumortextstr)
                    listofresult.append(0)
            else:
                for rumortext in news['data']:
                    rumortextstr=rumortext['features']
                    tweetIDtest.append(rumortext['tweetid'])

                    listofParatest.append(rumortextstr)
                    listofresulttest.append(0)
    # random.seed(0)
    # random.shuffle(listofPara)
    # random.seed(0)
    # random.shuffle(listofresult)

    trainX=np.array(listofPara)
    TrainY=np.array(listofresult)
    TestX=np.array(listofParatest)
    TextY=np.array(listofresulttest)



    X_train = pandas.DataFrame(trainX)[0]

    y_train = pandas.Series(TrainY)
    X_test = pandas.DataFrame(TestX)[0]
    y_test = pandas.Series(TextY)



    # Process vocabulary
    vocab_processor = learn.preprocessing.VocabularyProcessor(MAX_DOCUMENT_LENGTH)
    X_train = np.array(list(vocab_processor.fit_transform(X_train)))
    X_test = np.array(list(vocab_processor.transform(X_test)))
    n_words = len(vocab_processor.vocabulary_)
    # print('Total words: %d' % n_words)
    max_features = n_words
    maxlen = MAX_DOCUMENT_LENGTH  # cut texts after this number of words (among top max_features most common words)
    batch_size = 1000
    embedding_dims = 50
    nb_epoch = 10

# print('Loading data...')
#     (X_train, y_train), (X_test, y_test) = imdb.load_data(nb_words=max_features)
    print(len(X_train), 'train sequences')
    print(len(X_test), 'test sequences')
    print('Average train sequence length: {}'.format(np.mean(list(map(len, X_train)), dtype=int)))
    print('Average test sequence length: {}'.format(np.mean(list(map(len, X_test)), dtype=int)))
    ngram_range = 2

    if ngram_range > 1:
        print('Adding {}-gram features'.format(ngram_range))
        # Create set of unique n-gram from the training set.
        ngram_set = set()
        for input_list in X_train:
            for i in range(2, ngram_range+1):
                set_of_ngram = create_ngram_set(input_list, ngram_value=i)
                ngram_set.update(set_of_ngram)

        # Dictionary mapping n-gram token to a unique integer.
        # Integer values are greater than max_features in order
        # to avoid collision with existing features.
        start_index = max_features + 1
        token_indice = {v: k+start_index for k, v in enumerate(ngram_set)}
        indice_token = {token_indice[k]: k for k in token_indice}

        # max_features is the highest integer that could be found in the dataset.
        max_features = np.max(list(indice_token.keys())) + 1

        # Augmenting X_train and X_test with n-grams features
        print(X_train.shape)
        X_train = add_ngram(X_train, token_indice, ngram_range)
        X_test = add_ngram(X_test, token_indice, ngram_range)
        print('Average train sequence length: {}'.format(np.mean(list(map(len, X_train)), dtype=int)))
        print('Average test sequence length: {}'.format(np.mean(list(map(len, X_test)), dtype=int)))

    print('Pad sequences (samples x time)')
    X_train = sequence.pad_sequences(X_train, maxlen=maxlen)
    X_test = sequence.pad_sequences(X_test, maxlen=maxlen)
    print('X_train shape:', X_train.shape)
    print('X_test shape:', X_test.shape)

    print('Build model...')
    model = Sequential()

    # we start off with an efficient embedding layer which maps
    # our vocab indices into embedding_dims dimensions
    model.add(Embedding(max_features,
                        embedding_dims,
                        input_length=maxlen))

    # we add a GlobalAveragePooling1D, which will average the embeddings
    # of all words in the document
    model.add(GlobalAveragePooling1D())

    # We project onto a single unit output layer, and squash it with a sigmoid:
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])

    model.fit(X_train, y_train,
                  batch_size=batch_size,
                  nb_epoch=nb_epoch,
                  validation_data=(X_test, y_test),callbacks=[callbacks.EarlyStopping(monitor='val_acc', patience=0, verbose=0, mode='auto')])
    score, acc = model.evaluate(X_test, y_test,
                                batch_size=batch_size)
    print('Test score:', score)
    print('Test accuracy:', acc)