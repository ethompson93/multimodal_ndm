''' making a connectome class (maybe doesn't need to be a class but wanted to practise)'''

from src.prep_connectome import prep_connectome

class Connectome:
    '''connectome class - contains the name and filepath, and parameters for preprocessing'''
    def __init__(self, name, path, thr=0.1, inv=False, zero_neg=True):
        self.name = name
        self.path = path
        self.thr = thr
        self.inv = inv
        self.zero_neg = zero_neg

    def load_data(self, thr):
        ''' loads the connectome from its filename
            Parameters:
                thr : set the threshold for the connectome
            Returns:
                conn : square array of connectome
        '''
        conn = prep_connectome(self.path, thr, zero_neg=True, inv=self.inv)
        return conn
