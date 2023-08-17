'''load connectome and perform thresholding etc.'''
import numpy as np
import bct

def prep_connectome(connectome_fname,
                    thr=False,
                    remove_subcortical=False,
                    inv=False,
                    zero_neg=True):

    ''' reads connectome, makes symmetric
        Parameters:
            connectome_fname : path to the connectome
            thr : argument preserves a proportion thr (0<thr<1) of the strongest weights
            remove_subcortical : logical, if true subcortical elements are removed
            inv : inverts matrix elements
            zero_neg : if true, negative weights are set to zero. Otherwise use absolute values
        Returns:
            conn : pre-processed connectome
    '''

    conn = np.loadtxt(connectome_fname, delimiter=",")

    conn = np.triu(conn, 1) + np.tril(conn.T, -1)

    if zero_neg is False:
        conn = np.abs(conn)
    else:
        conn[conn<0] = 0

    # remove subcortical parcels
    if remove_subcortical is True:
        # specific to Desikan-Killiany atlas
        subcortical_idx = [34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 83]
        conn = np.delete(conn, subcortical_idx, axis=0)
        conn = np.delete(conn, subcortical_idx, axis=1)

    if inv is True:
        conn[conn == 0] = np.nan
        conn = 1 / conn
        conn = np.nan_to_num(conn, 0)

    # apply threshold
    if thr is not False:
        assert isinstance(thr, float)
        assert 0 < thr < 1
        conn = bct.threshold_proportional(conn, thr, copy=True)

    # standardise connectome
    conn = bct.weight_conversion(conn, "normalize", copy=True)

    return conn
