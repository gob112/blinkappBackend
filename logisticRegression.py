

import numpy as n


def sigmoid(func_z):
    return 1.0/ (1.0 + n.exp(-func_z))
    

def gradient_calculation(w_b,X,y):
    #w_b are the paremeters we are trying to find that best fits the data its a vectore the same size as X
    #X is a matrix with all feature inputs eg blink rate, IBM, and standard deviation of blink rate
    #y is the correct output
    
    m = y.size
    
    return (1/m) * (X.T @ (sigmoid(X @ w_b)) - y ) # derevative of the cost function


def gradient_decsent(X,y,a,iter,tolerance):
    #[[1, 2, 3, 4], [5, 6, 7, 8]]
    #.shape --> (2,4) --> two arrays where each has 4 elements
    
    x_b = n.c_[n.ones((X.shape[0],1), X)]
    w_b = n.zeros(x_b.shape[1])
    for i in range(iter):
        grad = gradient_calculation(w_b,X,y)
        w_b -= a * grad
        
        if n.linalg.norm(grad) < tolerance:
            break
    return w_b
def prediction(X,w_b,thresh):
    x_b = n.c_[n.ones((X.shape[0],1), X)]
    prob = sigmoid(x_b @ w_b)
    return (prob >= thresh).astype(int)
     