'''function to calculate sum of squared error between multi-dimensional variables'''
import numpy as np

def mysse(xx, yy):
    '''returns sum-of-squared errors between inputs xx and yy'''
    if xx.ndim == 1:
        xx = np.expand_dims(xx, 1)
    if yy.ndim == 1:
        yy = np.expand_dims(yy, 1)

    sse = np.sum((xx-yy)**2, axis=0)
    return sse
