

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
training_set = tf.contrib.learn.datasets.base.load_csv(filename=IRIS_TRAINING, target_dtype=np.float32,target_column=2,has_header=False)
test_set = tf.contrib.learn.datasets.base.load_csv(filename=IRIS_TEST, target_dtype=np.float32,target_column=2,has_header=False)
x_train, x_test, y_train, y_test = training_set.data, test_set.data,  training_set.target, test_set.target
print( (x_test[0] ))
print(y_test[0])
x = tf.placeholder(tf.float32, [None, 16])
W = tf.Variable(tf.zeros([16, 2]))
b = tf.Variable(tf.zeros([2]))
y = tf.nn.softmax(tf.matmul(x, W) + b)
y_ = tf.placeholder(tf.float32, [None, 2])
cross_entropy = -tf.reduce_sum(y_*tf.log(y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)








# Launch the graph in a session
with tf.Session() as sess:
    # you need to initialize all variables
    tf.initialize_all_variables().run()

    for i in range(1000):
        for start, end in zip(range(0, len(x_train), 128), range(128, len(x_train), 128)):
            sess.run(train_step, feed_dict={x: x_train[start:end],y_: y_train[start:end]})
    correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))

    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    print(sess.run(accuracy, feed_dict={x: x_test, y_: y_test}))
