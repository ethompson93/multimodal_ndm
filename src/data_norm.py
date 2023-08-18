'''function for normalising data'''
import numpy as np

def data_norm(raw_data):
    '''min-max normalise the data'''
    data_normed = (raw_data - np.min(raw_data))/(np.max(raw_data) - np.min(raw_data))
    return data_normed
    