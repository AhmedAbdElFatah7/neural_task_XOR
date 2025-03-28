# -*- coding: utf-8 -*-
"""Lab04_Logic_Gates_Neural_Networks (1).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HrienUeWbIWo5XW4_zINaFyA-Pco2AVd

# Setup
"""

# Commented out IPython magic to ensure Python compatibility.

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
#import itertools as it

# %matplotlib inline

"""# Neurons as Logic Gates

As an introduction to neural networks and their component neurons, we are going to look at using neurons to implement the most primitive logic computations:  logic gates.  Let's go!

##### The Sigmoid Function

The basic, classic activation function that we apply to neurons is a  sigmoid (sometimes just called *the* sigmoid function) function:  the standard logistic function.

$$
\sigma = \frac{1}{1 + e^{-x}}
$$

$\sigma$ ranges from (0, 1). When the input $x$ is negative, $\sigma$ is close to 0. When $x$ is positive, $\sigma$ is close to 1. At $x=0$, $\sigma=0.5$

We can implement this conveniently with NumPy.
"""

def sigmoid(x):
    """Sigmoid function"""
    return 1.0 / (1.0 + np.exp(-x))

"""And plot it with matplotlib."""

# Plot The sigmoid function
xs = np.linspace(-10, 10, num=100, dtype=np.float32)
activation = sigmoid(xs)

fig = plt.figure(figsize=(4,3))
plt.plot(xs, activation)
plt.plot(0,.5,'ro')

plt.grid(True, which='both')
plt.axhline(y=0, color='y')
plt.axvline(x=0, color='y')
plt.ylim([-0.1, 1.15])
plt.show()

xs = np.linspace(-10, 10, num=100, dtype=np.float32)
print(xs)

"""## An Example with OR

##### OR Logic
A logic gate takes in two boolean (true/false or 1/0) inputs, and returns either a 0 or 1 depending on its rule. The truth table for a logic gate shows the outputs for each combination of inputs: (0, 0), (0, 1), (1,0), and (1, 1). For example, let's look at the truth table for an Or-gate:

<table>
<tr><th colspan="3">OR gate truth table</th></tr>
<tr><th colspan="2">Input</th><th>Output</th></tr>
<tr><td>0</td><td>0</td><td>0</td></tr>
<tr><td>0</td><td>1</td><td>1</td></tr>
<tr><td>1</td><td>0</td><td>1</td></tr>
<tr><td>1</td><td>1</td><td>1</td></tr>
</table>

##### OR as a Neuron

A neuron that uses the sigmoid activation function outputs a value between (0, 1). This naturally leads us to think about boolean values. Imagine a neuron that takes in two inputs, $x_1$ and $x_2$, and a bias term:

   <img src="logic01.png" width=50% />

By limiting the inputs of $x_1$ and $x_2$ to be in $\left\{0, 1\right\}$, we can simulate the effect of logic gates with our neuron. The goal is to find the weights (represented by ? marks above), such that it returns an output close to 0 or 1 depending on the inputs.  What weights should we use to output the same results as OR? Remember: $\sigma(z)$ is close to 0 when $z$ is largely negative (around -10 or less), and is close to 1 when $z$ is largely positive (around +10 or greater).

$$
z = w_1 x_1 + w_2 x_2 + b
$$

Let's think this through:

* When $x_1$ and $x_2$ are both 0, the only value affecting $z$ is $b$. Because we want the result for input (0, 0) to be close to zero, $b$ should be negative (at least -10) to get the very left-hand part of the sigmoid.
* If either $x_1$ or $x_2$ is 1, we want the output to be close to 1. That means the weights associated with $x_1$ and $x_2$ should be enough to offset $b$ to the point of causing $z$ to be at least 10 (i.e., to the far right part of the sigmoid).

Let's give $b$ a value of -10. How big do we need $w_1$ and $w_2$ to be?  At least +20 will get us to +10 for just one of $\{w_1, w_2\}$ being on.

So let's try out $w_1=20$, $w_2=20$, and $b=-10$:

 <img src="logic02.png" width=50% />

##### Some Utility Functions
Since we're going to be making several example logic gates (from different sets of weights and biases), here are two helpers.  The first takes our weights and baises and turns them into a two-argument function that we can use like `and(a,b)`.  The second is for printing a truth table for a gate.
"""

# Logic gate function
def logic_gate(w1, w2, b, x1, x2):
  ''' logic_gate is a function which returns the results of
        taking two args and  (hopefully) acts like a logic gate (and/or/not/etc.).
        its behavior is determined by w1,w2,b. '''
  return sigmoid(w1 * x1 + w2 * x2 + b)

# Test function that takes a function with two arguments
def test_gate(w1, w2, b):
  for x1 in range(2):
    for x2 in range(2):
      print("{}, {}: {}".format(x1, x2, np.round(logic_gate(w1, w2, b, x1, x2))))

"""Let's see how we did.  Here's the gold-standard truth table.

<table>
<tr><th colspan="3">OR gate truth table</th></tr>
<tr><th colspan="2">Input</th><th>Output</th></tr>
<tr><td>0</td><td>0</td><td>0</td></tr>
<tr><td>0</td><td>1</td><td>1</td></tr>
<tr><td>1</td><td>0</td><td>1</td></tr>
<tr><td>1</td><td>1</td><td>1</td></tr>
</table>

And our result:
"""

or_gate = test_gate(20, 20, -10)

"""This matches - great!

# Exercise 1

##### Part 1:  AND Gate

Now you try finding the appropriate weight values for each truth table. Try not to guess and check. Think through it logically and try to derive values that work.

<table>
<tr><th colspan="3">AND gate truth table</th></tr>
<tr><th colspan="2">Input</th><th>Output</th></tr>
<tr><td>0</td><td>0</td><td>0</td></tr>
<tr><td>0</td><td>1</td><td>0</td></tr>
<tr><td>1</td><td>0</td><td>0</td></tr>
<tr><td>1</td><td>1</td><td>1</td></tr>
</table>
"""

# Fill in the w1, w2, and b parameters such that the truth table matches
# and_gate = test_gate(...)

"""##### Part 2: NOR (Not Or) Gate
<table>
<tr><th colspan="3">NOR gate truth table</th></tr>
<tr><th colspan="2">Input</th><th>Output</th></tr>
<tr><td>0</td><td>0</td><td>1</td></tr>
<tr><td>0</td><td>1</td><td>0</td></tr>
<tr><td>1</td><td>0</td><td>0</td></tr>
<tr><td>1</td><td>1</td><td>0</td></tr>
</table>
<table>
"""

# Fill in the w1, w2, and b parameters such that the truth table matches
# nor_gate = test_gate(...)

"""##### Part 3: NAND (Not And) Gate
<table>
<tr><th colspan="3">NAND gate truth table</th></tr>
<tr><th colspan="2">Input</th><th>Output</th></tr>
<tr><td>0</td><td>0</td><td>1</td></tr>
<tr><td>0</td><td>1</td><td>1</td></tr>
<tr><td>1</td><td>0</td><td>1</td></tr>
<tr><td>1</td><td>1</td><td>0</td></tr>
</table>
"""

# Fill in the w1, w2, and b parameters such that the truth table matches
# nand_gate = test_gate(...)

"""## Solutions 1"""

b = tf.Variable(tf.zeros([1]))
print(b.numpy)

"""# Learning a Logic Gate

We can use TensorFlow to try and teach a model to learn the correct weights and bias by passing in our truth table as training data.
"""

# Define LogicGate Model using tf.Module
class LogicGate(tf.Module):
    def __init__(self):
        super().__init__()
        self.built = False  # Track if model is initialized

    def __call__(self, x, train=True):
        # Initialize weights and bias on first call
        if not self.built:
            input_dim = x.shape[-1]  # Number of input features
            self.w = tf.Variable(tf.random.normal([input_dim, 1]), name="weights")
            self.b = tf.Variable(tf.zeros([1]), name="bias")
            self.built = True

        # Compute logits: z = Wx + b
        z = tf.add(tf.matmul(x, self.w), self.b)
        return tf.sigmoid(z)  # Apply sigmoid

# Loss function (Mean Squared Error)
def compute_loss(y_pred, y_true):
    return tf.reduce_mean(tf.square(y_pred - y_true))

# Training function
def train_model(model, x_train, y_train, learning_rate=0.5, epochs=5000):
  # Iterate over the training data
  for epoch in range(epochs):
    with tf.GradientTape() as tape:
      y_pred = model(x_train)  # Forward pass
      loss = compute_loss(y_pred, y_train)

    # Update the parameters with respect to the gradient calculations
    grads = tape.gradient(loss, model.variables)
    for g,v in zip(grads, model.variables):
      v.assign_sub(learning_rate * g)

    # Print progress every 1000 epochs
    if epoch % 1000 == 0:
      acc = compute_accuracy(model, x_train, y_train)
      print(f"Epoch {epoch}, Loss: {loss.numpy():.4f}, Accuracy: {acc:.4f}")

# Accuracy function
def compute_accuracy(model, x, y_true):
    y_pred = model(x, train=False)
    y_pred_rounded = tf.round(y_pred)
    correct = tf.equal(y_pred_rounded, y_true)
    return tf.reduce_mean(tf.cast(correct, tf.float32)).numpy()

# XOR truth table
xor_table = np.array([[0, 0, 0],
                      [0, 1, 1],
                      [1, 0, 1],
                      [1, 1, 0]], dtype=np.float32)

x_train = xor_table[:, :2]
y_train = xor_table[:, 2:]

# Train XOR gate model
model = LogicGate()
train_model(model, x_train, y_train)

# Display learned parameters
w1, w2 = model.w.numpy().flatten()
b = model.b.numpy().flatten()[0]
print(f"\nLearned weight for w1: {w1}")
print(f"Learned weight for w2: {w2}")
print(f"Learned bias: {b}")

# Test XOR predictions
y_pred = model(x_train, train=False).numpy().round().astype(np.uint8)
print("Predicted XOR Truth Table:")
print(np.column_stack((xor_table[:, :2], y_pred)))

"""# Limits of Single Neurons

If you've taken computer science courses, you may know that the XOR gates are the basis of computation. They can be used as half-adders, the foundation of being able to add numbers together. Here's the truth table for XOR:

##### XOR (Exclusive Or) Gate
<table>
<tr><th colspan="3">NAND gate truth table</th></tr>
<tr><th colspan="2">Input</th><th>Output</th></tr>
<tr><td>0</td><td>0</td><td>0</td></tr>
<tr><td>0</td><td>1</td><td>1</td></tr>
<tr><td>1</td><td>0</td><td>1</td></tr>
<tr><td>1</td><td>1</td><td>0</td></tr>
</table>

Now the question is, can you create a set of weights such that a single neuron can output this property?  It turns out that you cannot. Single neurons can't correlate inputs, so it's just confused. So individual neurons are out. Can we still use neurons to somehow form an XOR gate?

What if we tried something more complex:

 <img src="logic03.png" width=50% />

Here, we've got the inputs going to two separate gates: the top neuron is an OR gate, and the bottom is a NAND gate. The output of these gates is passed to another neuron, which is an AND gate. If you work out the outputs at each combination of input values, you'll see that this is an XOR gate!

XOR(A,B)=OR(A, B) AND NAND(A,B).
"""

# Make sure you have or_gate, nand_gate, and and_gate working from above
#def xor_gate(a, b):
#    c = or_gate(a, b)
#    d = nand_gate(a, b)
#    return and_gate(c, d)
#test(xor_gate)

"""Thus, we can see how chaining together neurons can compose more complex models than we'd otherwise have access to."""



"""# Exercise 2: Learning an XOR Gate

<img src="logic03.png" width=50% />
"""