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
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding
from keras.layers import LSTM
from keras.layers import Convolution1D, MaxPooling1D
from keras.datasets import imdb

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
pool_length = 4
nb_filter = 64
embedding_size=128
filter_length = 5
lstm_output_size = 70

for time in range(times):
    # if time <=3:
    #     continue
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
#
# print('Loading data...')
#     (X_train, y_train), (X_test, y_test) = imdb.load_data(nb_words=max_features)
    print(len(X_train), 'train sequences')
    print(len(X_test), 'test sequences')

    # print('Pad sequences (samples x time)')
    model = Sequential()
    model.add(Embedding(max_features, embedding_size, input_length=maxlen))
    model.add(Dropout(0.25))
    model.add(Convolution1D(nb_filter=nb_filter,
                            filter_length=filter_length,
                            border_mode='valid',
                            activation='relu',
                            subsample_length=1))
    model.add(MaxPooling1D(pool_length=pool_length))
    model.add(LSTM(lstm_output_size))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    # plot(model, to_file='model.png')

    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    print('Train...')
    model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=10,
              validation_data=(X_test, y_test),callbacks=[callbacks.EarlyStopping(monitor='val_loss', patience=0, verbose=0, mode='auto'),
                                callbacks.ModelCheckpoint(path.Featurepath+'weights/'+str(time)+'.weigt', monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=True, mode='auto'),

                                callbacks.TensorBoard(log_dir='./logs', histogram_freq=0)])
    score, acc = model.evaluate(X_test, y_test, batch_size=batch_size)
    print('Test score:', score)
    print('Test accuracy:', acc)