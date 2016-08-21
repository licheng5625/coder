

import tensorflow as tf
import numpy as np
import path
import json
from sklearn import datasets, metrics
IRIS_TRAINING = path.TweetJSONpath+"train.csv"
IRIS_TEST =path.TweetJSONpath+"test.csv"
def init_weights(shape):
    return tf.Variable(tf.random_normal(shape, stddev=0.01))


def read_data():
    listofrumor=list()
    listofnews=list()

    with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/datasingle.txt', mode='r') as writer:
        for line in writer:
            JSON=json.loads(line)
            listofrumor.append(JSON)


    with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/datasingleNewsBBC.txt', mode='r') as writer:
        for line in writer:
            JSON=json.loads(line)
            listofnews.append(JSON)
    with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/datasingleNews.txt', mode='r') as writer:
        for line in writer:
            JSON=json.loads(line)
            listofnews.append(JSON)

    lenthofrumor=len(listofrumor)
    print(lenthofrumor)
    lenthofnews=len(listofnews)

    print(lenthofnews)
    minsize=min(len(listofrumor),len(listofnews))
    mintrainsize=int(0.89*minsize)
    mintestsize=int(0.1*minsize)
    rumortrainsize=int(0.89*lenthofrumor)
    newstrainsize=int(0.89*lenthofnews)
    rumortestsize=int(0.1*lenthofrumor)
    newstestsize=int(0.1*lenthofnews)

    x_train=list()
    y_train=list()

    x_test=list()
    y_test=list()

    for i in range (0,rumortrainsize):#len(listofnews)-5):
        temp=[]
        temp=temp+listofrumor[i][:-1]#[indexoffeaturelow:indexoffeaturelow+1]
        x_train.append(temp)
        y_train.append([1])
    for i in range(0,newstrainsize):
        temp2=[]
        temp2=temp2+listofnews[i][:-1]#[indexoffeaturelow:indexoffeaturelow+1]
        x_train.append(temp2)
        y_train.append([0])

    # for i in range (0,20000):#len(listofnews)-5):
    #     temp2=[]
    #     temp2=temp2+listofnews[i][:-1]#[indexoffeaturelow:indexoffeaturelow+1]
    #     x_train.append(temp2)
    #     y_train.append([0,1])

    for i in range (rumortrainsize,lenthofrumor):
        temp=[]
        temp=temp+listofrumor[i][:-1]#[indexoffeaturelow:indexoffeaturelow+1]
        x_test.append(temp)
        y_test.append([1])
    for i in range (newstrainsize,lenthofnews):
        temp=[]
        temp=temp+listofnews[i][:-1]#[indexoffeaturelow:indexoffeaturelow+1]
        x_test.append(temp)
        y_test.append([0])
    x_train=np.array(x_train)
    y_train=np.array(y_train)
    x_test=np.array(x_test)
    y_test=np.array(y_test)
    # x_train=x_train[:16]
    # x_test=x_test[:16]


    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    # Don't cheat - fit only on training data
    scaler.fit(x_train)
    x_train = scaler.transform(x_train)
    # apply same transformation to test data
    x_test = scaler.transform(x_test)


    return x_train,y_train,x_test,y_test


x_train,y_train,x_test,y_test=read_data()

featureslethght=31
x = tf.placeholder(tf.float32, [None, featureslethght])
W = tf.Variable(tf.zeros([featureslethght, 1]))
b = tf.Variable(tf.zeros([1]))
y = tf.nn.softmax(tf.matmul(x, W) + b)
y_ = tf.placeholder(tf.float32, [None, 1])
cross_entropy = -tf.reduce_sum(y_*tf.log(y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)








# Launch the graph in a session
with tf.Session() as sess:
    # you need to initialize all variables
    tf.initialize_all_variables().run()

    for i in range(1000):
        for start, end in zip(range(0, len(x_train), 128), range(128, len(x_train), 128)):
            sess.run(train_step, feed_dict={x: x_train[start:end],y_: y_train[start:end]})
        if (i+1)%100==0:
            feed_dict = {x: x_test}
            score = metrics.accuracy_score(sess.run(y, feed_dict), (y_test))
            print(score)


    #         correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
    #
    #         accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    #
    #         print(str(i)+'   '+str(sess.run(accuracy, feed_dict={x: x_test, y_: y_test})))#0.663292
    #
    # correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
    #
    # accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    #
    # print(sess.run(accuracy, feed_dict={x: x_test, y_: y_test}))#0.663292

