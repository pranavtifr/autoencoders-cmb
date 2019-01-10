import tensorflow.contrib.layers as lays
from map_gen import *

batch_size = 500  # Number of samples in each batch
epoch_num = 20     # Number of epochs to train the network
lr = 0.01        # Learning rate
xres,yres,_ = get_res()
print(xres,yres,xres*yres)
def fcc_autoencoder(inputs):
    net = lays.fully_connected(inputs,500)
    net = lays.fully_connected(net,100)
    net = lays.fully_connected(net,500)
    net = lays.fully_connected(net,xres*yres)
    return net


def autoencoder(inputs):
    # encoder
    # 32 x 32 x 1   ->  16 x 16 x 32
    # 16 x 16 x 32  ->  8 x 8 x 16
    # 8 x 8 x 16    ->  2 x 2 x 8
    net = lays.conv2d(inputs, 32, [5, 5], stride=2, padding='SAME')
    net = lays.conv2d(net, 16, [5, 5], stride=2, padding='SAME')
    net = lays.conv2d(net, 8, [5, 5], stride=4, padding='SAME')
    net = lays.fully_connected(net,36)
    # decoder
    # 2 x 2 x 8    ->  8 x 8 x 16
    # 8 x 8 x 16   ->  16 x 16 x 32
    # 16 x 16 x 32  ->  32 x 32 x 1
    net = lays.fully_connected(net,48)
    net = lays.conv2d_transpose(net, 16, [5, 5], stride=4, padding='SAME')
    net = lays.conv2d_transpose(net, 32, [5, 5], stride=2, padding='SAME')
    net = lays.conv2d_transpose(net, 1, [5, 5], stride=2, padding='SAME', activation_fn=tf.nn.tanh)
    return net

import numpy as np

import tensorflow as tf

ae_inputs = tf.placeholder(tf.float32, (None, xres,yres, 1))  # input to the network (MNIST images)
ae_outputs = autoencoder(ae_inputs)  # create the Autoencoder network

# calculate the loss and optimize the network
loss = tf.reduce_mean(tf.square(ae_outputs - ae_inputs))  # claculate the mean square error loss
train_op = tf.train.AdamOptimizer(learning_rate=lr).minimize(loss)

# initialize the network
init = tf.global_variables_initializer()


# calculate the number of batches per epoch
batch_per_ep = 100
plotdata = []
plotdata2 = []
plotdata3 = []
data = []
for batch_n in range(batch_per_ep):
    data.append(give_skymap(batch_size))

with tf.Session() as sess:
    sess.run(init)
    for ep in range(epoch_num):  # epochs loop
        for batch_n in range(batch_per_ep):  # batches loop
            batch_img = data[batch_n]
            _, c = sess.run([train_op, loss], feed_dict={ae_inputs: batch_img})
        print('Epoch: {} - cost= {:.5f}'.format((ep + 1), c))

    # test the trained network with good data
        batch_img = give_skymap(batch_size)
        theloss = sess.run([loss], feed_dict={ae_inputs: batch_img})[0]
        plotdata.append([theloss,ep]) 
   # test with bad data
        #batch_img = give_badskymap(batch_size)
        #theloss = sess.run([loss], feed_dict={ae_inputs: batch_img})[0]
        #plotdata2.append([theloss,ep]) 

        batch_img = give_badskymap(batch_size,fnl=1e-3)
        theloss = sess.run([loss], feed_dict={ae_inputs: batch_img})[0]
        plotdata3.append([theloss,ep]) 
plotdata = np.array(plotdata)
#plotdata2 = np.array(plotdata2)
plotdata3 = np.array(plotdata3)
import matplotlib.pyplot as plt
plt.scatter(plotdata.T[1],plotdata.T[0],marker=".")
#plt.scatter(plotdata2.T[1],plotdata2.T[0],marker="x")
plt.scatter(plotdata3.T[1],plotdata3.T[0],marker="X")
plt.title('Loss vs Epoch')
plt.savefig('loss_scaling.png')
