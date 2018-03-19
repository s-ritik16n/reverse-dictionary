# implementing nn using numpy
import numpy as np

# input array
X = np.array([[1,0,1,0],[1,0,1,1],[0,1,0,1]])

# Output
y = np.array([[1],[1],[0]])

# sigmoid
def sigmoid(x):
    return 1/(1+np.exp(-x))

# derivative of sigmoid function
def der_sigmoid(x):
    return 1*(1-x)

# variable initialization
epoch=5000
lr=0.1
input_layer_neurons = X.shape[1] # number of features in data set
hiddenlayer_neurons = 3 # number of hidden layer neurons
output_neurons = 1

# weight and bias initialization
wh = np.random.uniform(size = (input_layer_neurons, hiddenlayer_neurons))
bh = np.random.uniform(size = (1,hiddenlayer_neurons))
wout = np.random.uniform(size = (hiddenlayer_neurons, output_neurons))
bout = np.random.uniform(size = (1, output_neurons))

for i in range(epoch):
    # Forward propagation
    hidden_layer_input1 = np.dot(X,wh)
    hidden_layer_input = hidden_layer_input1 + bh
    hidden_layer_activations = sigmoid(hidden_layer_input)
    output_layer_input1 = np.dot(hidden_layer_activations, wout)
    output_layer_input = output_layer_input1 + bout
    output = sigmoid(output_layer_input)

    # Backpropagation
    E = y-output
    slope_output_layer = der_sigmoid(output)
    slope_hidden_layer = der_sigmoid(hidden_layer_activations)
    d_output = E * slope_output_layer
    Error_at_hidden_layer = d_output.dot(wout.T)
    d_hiddenlayer = Error_at_hidden_layer * slope_hidden_layer
    wout += hidden_layer_activations.T.dot(d_output) * lr
    bout += np.sum(d_output, axis=0, keepdims = True) * lr
    wh += X.T.dot(d_hiddenlayer) * lr
    bh += np.sum(d_hiddenlayer, axis=0, keepdims = True) * lr

print(output)
