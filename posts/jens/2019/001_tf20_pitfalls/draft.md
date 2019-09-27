The release of Tensorflow 2.0 is supposedly around the corner (at the time of
writing, the current version is rc0), and with it comes the promise of a more
streamlined and intuitive API through things like full Keras integration and
eager execution. However, new ways of doing things also bring new problems. 
In this post, I want to summarize some common issues along with ways to avoid or
fix them.  Most of these come from own experience or questions on 
[Stackoverflow](https://stackoverflow.com/).  It is intended mostly as a 
compendium for new users and people taking our classes, but perhaps others 
can profit as well. Note that I might update this post in the future if more 
things come up (or there might be a part 2 instead)!


## tf.function

`tf.function` promises to make the switch between eager and graph mode easy --
develop, prototype and debug in eager execution and then slap on this decorator
for production-level performance. That's the idea -- in practice, there are so 
many quirks with this thing that one could write a whole series of posts on 
this alone -- and in fact 
[people have done so already](https://pgaleone.eu/tensorflow/tf.function/2019/03/21/dissecting-tf-function-part-1/).
That link points to a three-part post discussing this topic at length. I highly 
recommend reading it in detail, but I want to include some "highlights" here:

### Function arguments: Tensors vs Python types
To understand this issue, note what a `tf.function`-decorated function actually
does under the hood: The first time it is called, it is compiled into a graph, 
and then any other time the function will simply execute the graph instead -- 
the Python function is basically "ignored". Consider this simple example:

```python
@tf.function
def fun():
    print("hello")

fun()
fun()

>>>hello
```

As we can see, the print statement is only executed once even though we called
the function twice -- it doesn't make it into the compiled function.

This is, however, not the full story: Actually, the function is compiled _once 
for each input signature_ instead. This has dramatic implications if the 
function accepts Python numeric types, where each new value actually leads to a 
new input signature!! If this sounds a bit complicated, just consider the 
following example:

```python
import time

@tf.function
def fun(x, step):
    return 5*x

start = time.time()
for step in range(1000):
    dummy_fun(0, step)
stop = time.time()

print(stop-start)

>>>12.037055969238281
```

The function is compiled anew every time it is called with a new step count 
(which is every time we call it)! This will slow down execution dramatically.
Luckily, the fix is simple: Use tensors for such "changing values" instead, 
where different values do not count for a new input signature.

```python
start = time.time()
for step in tf.range(1000):
    dummy_fun(0, step)
stop = time.time()

print(stop-start)

>>>0.40102267265319824
```

So, whenever your decorated functions are conspicuously slow (especially if they
become *slower* after adding the decorator), you might want to check your input
parameters for Python numbers! Note that this is a fairly common scenario as we
may use step counters to control stuff like learning rate decay, saving a model
regularly etc.<dt-fn>In this case, simply removing the decorator and using
Python's `range` actually results in fastest performance (only 0.0006 seconds).
It seems like in this simple case, the overhead from even the first function
compilation as well as handling GPU data transfer with `tf.range` is too 
much. Sometimes it can pay off to stay eager!</dt-fn>


## GradientTape

Gradient tapes are a new kind of abstraction in TF 2.0. They basically replace 
`tf.gradient`. The idea is: With eager execution, there is no static 
computational graph, meaning no way to trace computations and thus no way to do 
backpropagation. Gradient tapes offer a way to temporarily trace computations as
needed so that we can still use TF's symbolic differentiation capabilities (it 
would be pretty useless otherwise!). Once again, however, it's easy to run into 
problems...

### Collecting variables before they exist
In TF 1.x, there is the concept of _collections_ that globally keep track of
things like trainable variables. In TF 2.0, this doesn't exist anymore: You need
to keep track of your variables yourself. Often, you will do this via 
`tf.keras.Model` instances, which have a convenient `trainable_variables` 
property. Consider this:

```python
model = tf.keras.Sequential([tf.keras.layers.Dense(10)])
var_list = model.trainable_variables

>>>ValueError: Weights for model sequential_1 have not yet been created. Weights
>>>are created when the Model is first called on inputs or `build()` is called 
>>>with an `input_shape`.
```

Whoops! The model was never built, so there are no variables. In the current 
version this leads to a crash, but older pre-releases actually executed 
perfectly fine -- but `model.trainable_variables` would be empty! This would 
mean that your fancy training loop just went through computing gradients for and
updating no variables at all... Thus, make sure you only ever use variable 
stores of your fully-built models:

```python
model = tf.keras.Sequential([tf.keras.layers.Dense(10)])
model.build((None, 784))  # for MNIST ;)
var_list = model.trainable_variables
```

Alternatively, always using `model.trainable_variables` explicitly (instead of a
shortcut assignment like above) can also prevent mistakes, but it can be
cumbersome in some situations.

### Optimizing things that are not variables
A common question is this: I want to find gradients with respect to the _input_ 
to my network, e.g. to find how sensitive the predictions are to certain parts
of the input, with the network itself staying fixed. I tried this but it doesn't
work:

```python
input_ = ...  # just get a tensor from somewhere
model = ...  # same for the model

with tf.GradientTape() as tape:
    # let's say we are interested in the class with index 7
    logits_seven = model(input_)[:, 7]
grad_for_inp = tape.gradient(logits_seven, input_)

print(grad_for_inp)

>>>None
```

The issue lies with what kind of computations `GradientTape` actually traces: By
default, it will store all computations related to any `tf.Variable` it comes 
across, _and nothing else_. In particular, since your network input is usually 
just a `Tensor` and not stored in a variable, related computations are not 
traced and so no gradients can be computed.<dt-fn>This is likely another case 
where raising an error would be preferable, but currently it just returns `None`
as a gradient....</dt-fn> Once again, the fix is actually really simple: You 
need to tell the tape what to trace (or "watch")!

```python
with tf.GradientTape(watch_accessed_variables=False) as tape:
    tape.watch(input_)
    logits_seven = model(input_)[:, 7]
grad_for_inp = tape.gradient(logits_seven, input_)

print(grad_for_inp)

>>>tf.Tensor(
>>>[[[[ 0.03662432 -0.0254075   0.06999005]
>>>   [ 0.00372662 -0.0231829   0.01369272]
>>>   [-0.06823001 -0.0217168  -0.02034823]
>>>   ...
```

Note that I passed an extra parameter to tell the tape _not_ to trace the
variables it comes across (i.e. all the model parameters). This isn't necessary 
for correctness, but should make the whole thing a little more efficient.

### Doing "computations" outside the tape context
Here's the example from above again:

```python
with tf.GradientTape() as tape:
    tape.watch(input_)
    logits = model(input_)
grad_for_eight = tape.gradient(logits[:, 7], input_)

print(grad_for_eight)

>>>None
```

It broke again! What happened? Note that this time, I do the indexing into the
"interesting" class _outside_ of the gradient tape context. This means that the
tape basically loses track of where this tensor came from and cannot compute
the gradients anymore. As a rule of thumb, anything you put into `tape.gradient`
should come _straight_ out of the tape context without any modifications!
Another common example would be when you have multiple losses (e.g. 
classification and regularization losses) and add them to a "total loss" 
_outside_ the tape context. This won't work!

## Keras

Keras is "the" high-level interface in TF 2.0, and it is arguably much more 
convenient than the cumbersome `Estimator` interface or chaining `tf.layers`.
But once again, it does not come without pitfalls...

### Choosing the wrong variables to optimize
If using batch normalization, you might get strange warnings like this one:
```python
>>>W0924 09:53:23.799460 140659773245184 optimizer_v2.py:979] Gradients d does not 
>>>exist for variables ['batch_normalization_1/moving_mean:0', 
>>>'batch_normalization_1/moving_variance:0'] when minimizing the loss.
```

Looking at the code, it may well include something like this:

```python
grads = tape.gradient(xent, model.variables)
optimizer.apply_gradients(zip(grads, model.variables))
```

This can be subtle: We are using `model.variables` instead of 
`trainable_variables`. These are different! `variables` stores anything that
has a "state" that needs to be stored over the course of time. In the case of
batchnorm, this includes the "population statistics" batchnorm uses during 
inference (instead of minibatch statistics). These are not used during training
and so no gradients can be computed (and you wouldn't want this anyway!).

There are of course other cases besides batchnorm, but the root cause is often
the same: You are including variables in your optimization procedure that have
no business of being there. Often, using `model.trainable_variables` can fix
this.

### Using numpy where you shouldn't
Keras models have functionality that allows us to easily execute the full model
in a single line. How about this (re-using an example from above)?

```python
with tf.GradientTape(watch_accessed_variables=False) as tape:
    tape.watch(input_)
    logits_seven = model.predict(input_)[:, 7]
grad_for_inp = tape.gradient(logits_seven, input_)

print(grad_for_inp)

>>>AttributeError: 'numpy.dtype' object has no attribute 'is_floating'
```

Why does this fail? All we wanted to do was the forward pass of the model. It
turns out that `model.predict` returns a numpy array, and this quite literally
interrupts the "tensor flow", meaning no gradients can be computed 
either.<dt-fn>Although to be precise, this specific error is due to a different
reason.</dt-fn>
Instead, make sure to always use Keras models as callables as in the examples
above. This still holds if you try to be smart and "just go back to Tensorflow"
again:

```python
with tf.GradientTape(watch_accessed_variables=False) as tape:
    tape.watch(input_)
    logits_seven = model.predict(input_)[:, 7]
    logits = tf.convert_to_tensor(logits)
grad_for_inp = tape.gradient(logits_seven, input_)

print(grad_for_inp)

>>>None
```

Do note that this applies to _anything_ involving numpy arrays -- gradients
cannot propagate through these operations!! This has always been the case, but
is arguably a bigger problem in TF 2.0 where it is so tempting to mix between
eager execution and numpy arrays.
