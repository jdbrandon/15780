import numpy as np
import struct

def parse_images(filename):
    f = open(filename,"rb");
    magic,size = struct.unpack('>ii', f.read(8))
    sx,sy = struct.unpack('>ii', f.read(8))
    X = []
    for i in range(size):
        im =  struct.unpack('B'*(sx*sy), f.read(sx*sy))
        X.append([float(x)/255.0 for x in im]);
    return np.array(X);

def parse_labels(filename):
    one_hot = lambda x, K: np.array(x[:,None] == np.arange(K)[None, :], 
                                    dtype=np.float64)
    f = open(filename,"rb");
    magic,size = struct.unpack('>ii', f.read(8))
    return one_hot(np.array(struct.unpack('B'*size, f.read(size))), 10)

def error(y_hat,y):
    return float(np.sum(np.argmax(y_hat) != 
                        np.argmax(y)))/y.shape[0]



# function calls to load data (uncomment to load MINST data)
#X_train = parse_images("train-images-idx3-ubyte")
#y_train = parse_labels("train-labels-idx1-ubyte")
#X_test = parse_images("t10k-images-idx3-ubyte")
#y_test = parse_labels("t10k-labels-idx1-ubyte")


# helper functions for loss and neural network activations
softmax_loss = lambda yp,y : (np.log(np.sum(np.exp(yp))) - yp.dot(y), 
                              np.exp(yp)/np.sum(np.exp(yp)) - y)
f_tanh = lambda x : (np.tanh(x), 1./np.cosh(x)**2)
f_relu = lambda x : (np.maximum(0,x), (x>=0).astype(np.float64))
f_lin = lambda x : (x, np.ones(x.shape))


# set up a simple deep neural network for MNIST task
np.random.seed(0)
#layer_sizes = [784, 400, 200, 100, 10]
layer_sizes = [784, 200, 100, 10]
W = [0.1*np.random.randn(n,m) for m,n in zip(layer_sizes[:-1], layer_sizes[1:])]
b = [0.1*np.random.randn(n) for n in layer_sizes[1:]]
f = [f_relu]*(len(layer_sizes)-2) + [f_lin]


##### Implement the functions below this point ######

def softmax_gd(X, y, Xt, yt, epochs=10, alpha = 0.5):
    """ 
    Run gradient descent to solve linear softmax regression.
    
    Inputs:
        X: numpy array of training inputs
        y: numpy array of training outputs
        Xt: numpy array of testing inputs
        yt: numpy array of testing outputs
        epochs: number of passes to make over the whole training set
        alpha: step size
        
    Outputs:
        Theta: 10 x 785 numpy array of trained weights
    """
    print "Test Err\tTrain Err\tTest Loss\tTrain Loss\tEpoch"
    X = np.insert(X, len(X[0]), [1], axis = 1)
    Xt = np.insert(Xt, len(Xt[0]), [1], axis = 1)
    theta = np.zeros((epochs,len(X[0])))
    for t in range(epochs):#10
        avgLoss = 0
        e = 0
        for i in range(len(Xt)):
            loss,_ = softmax_loss(theta.dot(Xt[i]), yt[i])
            avgLoss += loss
            e += error(theta.dot(Xt[i]), yt[i])
        testLoss = avgLoss/len(Xt)
        testErr = e/len(Xt)
        avgLoss = 0
        e = 0
        g = np.zeros((epochs,len(X[0])))
        for i in range(len(X)):#6000
            loss, gradient = softmax_loss(theta.dot(X[i]), y[i])
            g += np.outer(gradient, X[i])/len(X)
            avgLoss += loss
            e += error(theta.dot(X[i]),y[i])
        print "%.6f\t%.6f\t%.6f\t%.6f\t%d" % (testErr, e/len(X), testLoss,avgLoss/len(X), t)
        theta -= alpha * g 

    return theta


def softmax_sgd(X,y, Xt, yt, epochs=10, alpha = 0.01):
    """ 
    Run stoachstic gradient descent to solve linear softmax regression.
    
    Inputs:
        X: numpy array of training inputs
        y: numpy array of training outputs
        Xt: numpy array of testing inputs
        yt: numpy array of testing outputs
        epochs: number of passes to make over the whole training set
        alpha: step size
        
    Outputs:
        Theta: 10 x 785 numpy array of trained weights
    """
    print "Test Err\tTrain Err\tTest Loss\tTrain Loss\tEpoch"
    X = np.insert(X, len(X[0]), [1], axis = 1)
    Xt = np.insert(Xt, len(Xt[0]), [1], axis = 1)
    theta = np.zeros((epochs,len(X[0])))
    for t in range(epochs):#10
        avgLoss = 0
        e = 0
        for i in range(len(Xt)):
            loss,_ = softmax_loss(theta.dot(Xt[i]), yt[i])
            avgLoss += loss
            e += error(theta.dot(Xt[i]), yt[i])
        testLoss = avgLoss/len(Xt)
        testErr = e/len(Xt)
        avgLoss = 0
        e = 0
        for i in range(len(X)):#6000
            loss, gradient = softmax_loss(theta.dot(X[i]), y[i])
            avgLoss += loss
            e += error(theta.dot(X[i]), y[i])
            theta -= alpha * np.outer(gradient, X[i])
        print "%.6f\t%.6f\t%.6f\t%.6f\t%d" % (testErr, e/len(X), testLoss, avgLoss/len(X), t)

    return theta


def nn(x, W, b, f):
    """
    Compute output of a neural network.
    
    Input:
        x: numpy array of input
        W: list of numpy arrays for W parameters
        b: list of numpy arraos for b parameters
        f: list of activation functions for each layer
        
    Output:
        z: list of activationsn, where each element in the list is a tuple:
           (z_i, z'_i)
           for z_i and z'_i each being a numpy array of activations/derivatives
    """
    z = []
    z.append((x,np.zeros(np.shape(x))))
    t = x
    for i in range(len(W)):
        t, gv = f[i](W[i].dot(t) + b[i])
        z.append((t, gv))
    return z


def nn_loss(x, y, W, b, f):
    """
    Compute loss of a neural net prediction, plus gradients of parameters
    
    Input:
        x: numpy array of input
        y: numpy array of output
        W: list of numpy arrays for W parameters
        b: list of numpy arrays for b parameters
        f: list of activation functions for each layer
        
    Output tuple: (L, dW, db)
        L: softmax loss on this example
        dW: list of numpy arrays for gradients of W parameters
        db: list of numpy arrays for gradients of b parameters
    """
    z = nn(x,W,b,f)
    g = [0] * len(z)
    dW = [0] * len(z)
    db = [0] * len(z)
    L, g[-1] = softmax_loss(z[-1][0], y)
    for i in xrange(len(W)-1, -1, -1):
        tmp = g[i+1] * z[i+1][1]
        g[i] = W[i].T.dot(tmp)
        db[i] = tmp
        dW[i] = np.outer(tmp, z[i][0])
    
    return (L, dW, db, z)

            
def nn_sgd(X,y, Xt, yt, W, b, f, epochs=10, alpha = 0.01):
    """ 
    Run stoachstic gradient descent to solve linear softmax regression.
    
    Inputs:
        X: numpy array of training inputs
        y: numpy array of training outputs
        Xt: numpy array of testing inputs
        yt: numpy array of testing outputs
        W: list of W parameters (with initial values)
        b: list of b parameters (with initial values)
        f: list of activation functions
        epochs: number of passes to make over the whole training set
        alpha: step size
        
    Output: None (you can directly update the W and b inputs in place)
    """
    print "Test Err\tTrain Err\tTest Loss\tTrain Loss\tEpoch"
    for t in range(epochs):#10
        avgLoss = 0
        e = 0
        for i in range(len(Xt)):
            loss, _, _, z = nn_loss(Xt[i], yt[i], W, b, f)
            avgLoss += loss
            e += error(z[-1][0], yt[i])

        testLoss = avgLoss/len(Xt)
        testErr = e/len(Xt)
        e = 0
        avgLoss = 0
        for i in range(len(X)):#6000
            loss, dW, db, z = nn_loss(X[i], y[i], W, b, f)
            for j in range(len(W)):
                W[j] -= alpha * dW[j]
                b[j] -= alpha * db[j]
            avgLoss += loss
            e += error(z[-1][0],y[i])

        print "%.6f\t%.6f\t%.6f\t%.6f\t%d" % (testErr, e/len(X), testLoss,avgLoss/len(X), t)
    return 

#softmax_gd(X_train, y_train, X_test, y_test)
#softmax_sgd(X_train, y_train, X_test, y_test)
#nn_sgd(X_train, y_train, X_test, y_test, W, b, f)
