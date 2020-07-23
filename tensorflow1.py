

#tf.disable_v2_behavior()
import tensorflow.compat.v1 as tf
tf.disable_eager_execution()

# To support both python 2 and python 3
#from __future__ import division, print_function, unicode_literals

# Common imports
import numpy as np
import os
from tensorflow.python.framework import ops

# to make this notebook's output stable across runs
def reset_graph(seed=42):
    ops.reset_default_graph()
    tf.set_random_seed(seed)
    np.random.seed(seed)


# Much better code
# Using a function to build the ReLUs

reset_graph()


def relu(X):
    with tf.name_scope("relu"):
        w_shape = (int(X.get_shape()[1]), 1)
        w = tf.Variable(tf.random_normal(w_shape), name="weights")
        b = tf.Variable(0.0, name="bias")
        z = tf.add(tf.matmul(X, w), b, name="z")
        return tf.maximum(z, 0., name="max")


n_features = 3
X = tf.placeholder(tf.float32, shape=(None, n_features), name="X")
relus = [relu(X) for i in range(5)]
output = tf.add_n(relus, name="output")

file_writer = tf.summary.FileWriter("tf_logs/relu2", tf.get_default_graph())
file_writer.close()