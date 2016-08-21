
import json
import tensorflow as tf
import numpy as np
import path
from sklearn import datasets, metrics
IRIS_TRAINING = path.TweetJSONpath+"train.csv"
IRIS_TEST =path.TweetJSONpath+"test.csv"
def init_weights(shape):
    return tf.Variable(tf.random_normal(shape, stddev=0.01))


def model(X, w_h, w_h2, w_o, p_keep_input, p_keep_hidden): # this network is the same as the previous one except with an extra hidden layer + dropout
    X = tf.nn.dropout(X, p_keep_input)
    h = tf.nn.relu(tf.matmul(X, w_h))

    h = tf.nn.dropout(h, p_keep_hidden)
    h2 = tf.nn.relu(tf.matmul(h, w_h2))

    h2 = tf.nn.dropout(h2, p_keep_hidden)

    return tf.matmul(h2, w_o)





# Load datasets.
# training_set = tf.contrib.learn.datasets.base.load_csv(filename=IRIS_TRAINING, target_dtype=np.float32,target_column=2,has_header=False)
# test_set = tf.contrib.learn.datasets.base.load_csv(filename=IRIS_TEST, target_dtype=np.float32,target_column=2,has_header=False)
# x_train, x_test, y_train, y_test = training_set.data, test_set.data,  training_set.target, test_set.target

listofrumor=list()
listofnews=list()

with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/rumorsingletest.txt', mode='r') as writer:
    for line in writer:
        JSON=json.loads(line)
        listofrumor.append(JSON)

with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/newssingletest.txt', mode='r') as writer:
    for line in writer:
        JSON=json.loads(line)
        listofnews.append(JSON)

print(len(listofnews))


x_train=list()
y_train=list()

x_test=list()
y_test=list()

for i in range (0,20000):#len(listofnews)-5):
    temp=[]
    temp=temp+listofrumor[i][:-1]#[indexoffeaturelow:indexoffeaturelow+1]
    x_train.append(temp)
    y_train.append([1,0])

for i in range (0,20000):#len(listofnews)-5):
    temp2=[]
    temp2=temp2+listofnews[i][:-1]#[indexoffeaturelow:indexoffeaturelow+1]
    x_train.append(temp2)
    y_train.append([0,1])

for i in range (len(listofnews)-1000,len(listofnews)):
    temp=[]
    temp=temp+listofrumor[i][:-1]#[indexoffeaturelow:indexoffeaturelow+1]
    x_test.append(temp)
    y_test.append([1,0])
# for i in range (len(listofnews)-1000,len(listofnews)):
#     temp=[]
#     temp=temp+listofnews[i][:-1]#[indexoffeaturelow:indexoffeaturelow+1]
#     x_test.append(temp)
#     y_test.append([0,1])


x_train=np.asarray(x_train, dtype=np.float64)
y_train=np.asarray(y_train, dtype=np.float64)


y_test=np.asarray(y_test, dtype=np.float64)
x_test=np.asarray(x_test, dtype=np.float64)

numr=0
numn=0
for i in range(len(y_test)):
    if y_test[i][1]==1:
        numr+=1
    else:
        numn+=1
print(float(numn)/(numr+numn))



x = tf.placeholder("float", [None, 31])
y = tf.placeholder("float", [None, 2])

w_h = init_weights([31, 30])
w_h2 = init_weights([30, 30])
w_o = init_weights([30, 2])




p_keep_input = tf.placeholder("float")
p_keep_hidden = tf.placeholder("float")
py_x = model(x, w_h, w_h2, w_o, p_keep_input, p_keep_hidden)

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(py_x, y))
train_op = tf.train.RMSPropOptimizer(0.001, 0.9).minimize(cost)
predict_op = tf.argmax(py_x, 1)







# Launch the graph in a session
with tf.Session() as sess:
    # you need to initialize all variables
    tf.initialize_all_variables().run()

    for i in range(100):
        for start, end in zip(range(0, len(x_train), 128), range(128, len(x_train), 128)):
            sess.run(train_op, feed_dict={x: x_train[start:end],y: y_train[start:end],p_keep_input: 0.8, p_keep_hidden: 0.5})

        print(i, np.mean(np.argmax(y_test, axis=1) ==
             sess.run(predict_op, feed_dict={x: x_test, y: y_test,
                                             p_keep_input: 0.8,
                                             p_keep_hidden:  0.5})))

