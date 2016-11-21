#  Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""L."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import json
import mypath as path
import numpy as np
import pandas
from sklearn import metrics
import tensorflow as tf
from tensorflow.contrib import learn
import random
FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_bool('test_with_fake_data', False,
                         'Test the example code with fake data.')
tf.logging.set_verbosity(tf.logging.INFO)

MAX_DOCUMENT_LENGTH = 20
EMBEDDING_SIZE = 50
n_words = 0
outputFile=path.Featurepath+'tweetRNN30002.txt'


def bag_of_words_model(x, y):
  """A bag-of-words model. Note it disregards the word order in the text."""
  target = tf.one_hot(y, 15, 1, 0)
  word_vectors = learn.ops.categorical_variable(x, n_classes=n_words,
      embedding_size=EMBEDDING_SIZE, name='words')
  features = tf.reduce_max(word_vectors, reduction_indices=1)
  prediction, loss = learn.models.logistic_regression(features, target)
  train_op = tf.contrib.layers.optimize_loss(
      loss, tf.contrib.framework.get_global_step(),
      optimizer='Adam', learning_rate=0.01)
  return {'class': tf.argmax(prediction, 1), 'prob': prediction}, loss, train_op


def rnn_model(x, y):
  """Recurrent neural network model to predict from sequence of words
  to a class."""
  # Convert indexes of words into embeddings.
  # This creates embeddings matrix of [n_words, EMBEDDING_SIZE] and then
  # maps word indexes of the sequence into [batch_size, sequence_length,
  # EMBEDDING_SIZE].
  word_vectors = learn.ops.categorical_variable(x, n_classes=n_words,
      embedding_size=EMBEDDING_SIZE, name='words')

  # Split into list of embedding per word, while removing doc length dim.
  # word_list results to be a list of tensors [batch_size, EMBEDDING_SIZE].
  word_list = tf.unpack(word_vectors, axis=1)

  # Create a Gated Recurrent Unit cell with hidden size of EMBEDDING_SIZE.
  cell = tf.nn.rnn_cell.GRUCell(EMBEDDING_SIZE)
  cell = tf.nn.rnn_cell.MultiRNNCell([cell] * 2, state_is_tuple=True)

  # Create an unrolled Recurrent Neural Networks to length of
  # MAX_DOCUMENT_LENGTH and passes word_list as inputs for each unit.
  _, encoding = tf.nn.rnn(cell, word_list, dtype=tf.float32)
  target = tf.one_hot(y, 15, 1, 0)
  print(encoding)
  # # loss_weights = [tf.ones(1) for i in range(EMBEDDING_SIZE)]
  # loss = tf.nn.seq2seq.sequence_loss_by_example([encoding],  [tf.reshape(y, [-1])],  [tf.ones([EMBEDDING_SIZE])])
  # loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(encoding, target))

  # Given encoding of RNN, take encoding of last step (e.g hidden size of the
  # neural network of last step) and pass it as features for logistic
  # regression over output classes.
  # print(encoding)
  prediction, loss = learn.models.logistic_regression(encoding[-1] , target)

  # Create a trailossning op.
  train_op = tf.contrib.layers.optimize_loss(
      loss, tf.contrib.framework.get_global_step(),
      optimizer='Adam', learning_rate=0.01)
  # return {},loss, train_op
  return {'class': tf.argmax(prediction, 1), 'prob': prediction}, loss, train_op
def loadTEXT(time,times):
    indeslixt=[]
    with open(path.Featurepath+'indexshuffled.txt',encoding='utf-8',mode='r') as writer:
        indeslixt=json.loads(writer.read())

    listofrumor=[]
    listofnews=[]
    listofPara=list()
    listofresult=list()

    listofParatest=list()
    listofresulttest=list()
    lenofpiece=int(len(indeslixt)/times+0.5)

    with open(path.Featurepath+'featuresrumorsTextlable.txt', mode='r') as writer:
        for line in writer:
            JSON=json.loads(line)
            listofrumor.append(JSON)

    with open(path.Featurepath+'featuresNewsTextlable.txt', mode='r') as writer:
        for line in writer:
            JSON=json.loads(line)
            listofnews.append(JSON)
    for rumor in listofrumor:
                if rumor['eventID'] not in  indeslixt[time*lenofpiece: time*lenofpiece+lenofpiece]:
                    for rumortext in rumor['data']:
                        rumortext=str(rumortext)
                        listofPara.append(rumortext)
                        listofresult.append(1)
                else:
                    for rumortext in rumor['data']:
                        rumortext=str(rumortext)

                        listofParatest.append(rumortext)
                        listofresulttest.append(1)
    for rumor in listofnews:
                if rumor['eventID'] not in  indeslixt[time*lenofpiece: time*lenofpiece+lenofpiece]:
                    for rumortext in rumor['data']:
                        rumortext=str(rumortext)

                        listofPara.append(rumortext)
                        listofresult.append(0)
                else:
                    for rumortext in rumor['data']:
                        rumortext=str(rumortext)
                        listofParatest.append(rumortext)
                        listofresulttest.append(0)

    listofresulttest=np.array(listofresulttest)
    listofParatest=np.array(listofParatest)
    listofPara=np.array(listofPara)
    listofresult=np.array(listofresult)
    return listofPara,listofresult,listofParatest,listofresulttest
def main(unused_argv):
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

        listofPara=list()
        listofresult=list()

        listofParatest=list()
        listofresulttest=list()
        tweetIDtest=[]
        if 211 not in indeslixt[time*lenofpiece: time*lenofpiece+lenofpiece]:
            continue
        for rumor in listofrumor:
                if random.randint(1, 100)>choice:
                    continue
                if rumor['eventID'] not in  indeslixt[time*lenofpiece: time*lenofpiece+lenofpiece]:
                    for rumortext in rumor['data']:
                        rumortextstr=rumortext['features']
                        listofPara.append(rumortextstr)
                        listofresult.append(1)
                else:
                    if rumor['eventID']!=211:
                        continue
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

        trainX=np.array(listofPara)
        TrainY=np.array(listofresult)
        TestX=np.array(listofParatest)
        TextY=np.array(listofresulttest)



        x_train = pandas.DataFrame(trainX)[0]

        y_train = pandas.Series(TrainY)
        x_test = pandas.DataFrame(TestX)[0]
        y_test = pandas.Series(TextY)



        # Process vocabulary
        vocab_processor = learn.preprocessing.VocabularyProcessor(MAX_DOCUMENT_LENGTH)
        x_train = np.array(list(vocab_processor.fit_transform(x_train)))
        x_test = np.array(list(vocab_processor.transform(x_test)))
        n_words = len(vocab_processor.vocabulary_)
        print('Total words: %d' % n_words)
        validation_metrics = {"accuracy": tf.contrib.metrics.streaming_accuracy,
                      "precision": tf.contrib.metrics.streaming_precision,
                      "recall": tf.contrib.metrics.streaming_recall}

        val_monitor = tf.contrib.learn.monitors.ValidationMonitor(x_test, y_test,
                                                early_stopping_rounds=200,
                                                 )

        # Build model
        classifier = learn.Estimator(model_fn=rnn_model)
        print('Total data: %d' % len(x_train))
        # Train and predict
        classifier.fit(x_train, y_train, steps=6000,batch_size=10000 ,monitors=[val_monitor])
        y_predicted = [
          p['class'] for p in classifier.predict(x_test, as_iterable=True)]
        score = metrics.accuracy_score(y_test, y_predicted)
        recall+=metrics.recall_score(y_test, y_predicted)
        print(recall)
        for num in range(len(tweetIDtest)):
            tweetresult[tweetIDtest[num]]=str(y_predicted[num])
        correctword+=score*len(listofParatest)
        totleword+=len(y_test)
        print('Accuracy: {0:f}'.format(score))
    with open(outputFile, mode='w') as writer:
        JSON=json.dumps(tweetresult)
        writer.write(JSON + '\n')
    print('totle Accuracy: {0:f}'.format(float(correctword)/totleword))
    print(recall)

if __name__ == '__main__':
  tf.app.run()
