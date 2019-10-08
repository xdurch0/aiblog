This tutorial is based on [one that previously found on the Tensorflow website.](https://github.com/tensorflow/tensorflow/blob/r1.4/tensorflow/docs_src/get_started/mnist/beginners.md)
You can check that one for additional conceptual guidance, however the code
snippets found there are intended for old Tensorflow versions (1.x). Since the
official TF website is now lacking a comparable tutorial (the simple MNIST
tutorials use Keras instead of low-level concepts), the following is supposed
to offer an updated version working in Tensorflow 2.0. It is intended as a 
supplementary tutorial for 
[Assignment 1 of our Deep Learning class](https://ovgu-ailab.github.io/idl2019/ass1.html)
and assumes that you already went through the other posts linked there.


## Walkthrough

### Preparation
Download [this simple dataset class](https://ovgu-ailab.github.io/idl2019/assignments/1/datasets.py)
and put it in the same folder as your script/notebook. It's just a wrapper for
simple production of random minibatches of data.

### Imports

```python
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from datasets import MNISTDataset
```

### Loading data and sanity checking
We make use of the "built-in" MNIST data in Tensorflow. We plot the first
training image just so we know what we're dealing with -- it should be a 5. Feel
free to plot more images (and print the corresponding labels) to get to know the
data! Next, we create a dataset via our simple wrapper, using a batch size of 128.
Be aware that the data is originally represented as `uint8` in the range
`[0, 255]` but `MNISTDataset` converts it to `float32` in `[0,1]` by default.
Also, labels are converted from `uint8` to `int32`.

```python
mnist = tf.keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

plt.imshow(train_images[0], cmap="Greys_r")

data = MNISTDataset(train_images.reshape([-1, 784]), train_labels, 
                    test_images.reshape([-1, 784]), test_labels,
                    batch_size=128)
```

### Setting up for training
We decide on the number of training steps and the learning rate, and set up our
weights to be trained with random initial values (and zero biases).

```python
train_steps = 1000
learning_rate = 0.1

W = tf.Variable(np.zeros([784, 10]).astype(np.float32))
b = tf.Variable(np.zeros(10, dtype=np.float32))
```

### Training
The main training loop, using cross-entropy as a loss function. We regularly
print the current loss and accuracy to check progress.

Note that we compute the "logits", which is the common name for pre-softmax
values. They can be interpreted as log unnormalized probabilities and represent a 
"score" for each class.

In computing the accuracy, notice that we have to fiddle around with dtypes quite
a bit -- this is unfortunately common in Tensorflow.

```python
for step in range(train_steps):
    img_batch, lbl_batch = data.next_batch()
    with tf.GradientTape() as tape:
        logits = tf.matmul(img_batch, W) + b
        xent = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(
            logits=logits, labels=lbl_batch))
        
    grads = tape.gradient(xent, [W, b])
    W.assign_sub(learning_rate * grads[0])
    b.assign_sub(learning_rate * grads[1])
    
    if not step % 100:
        preds = tf.argmax(logits, axis=1, output_type=tf.int32)
        acc = tf.reduce_mean(tf.cast(tf.equal(preds, lbl_batch),
                             tf.float32))
        print("Loss: {} Accuracy: {}".format(xent, acc))
```

### Predicting/testing
We can use the trained model to predict labels on the test set and check the
model's accuracy. You should get around 0.9 (90%) here.

```python
test_preds = tf.argmax(tf.matmul(data.test_data, W) + b, axis=1,
                       output_type=tf.int32)
acc = tf.reduce_mean(tf.cast(tf.equal(test_preds, data.test_labels),
                             tf.float32))
print(acc)
```
