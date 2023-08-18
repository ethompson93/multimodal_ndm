'''function to convert seed name to indices in left and right hemisphere'''
def seed2idx(seed, ref_list):
    '''
    Parameters:
        seed: string eg. "Entorhinal"
        ref_list: list containing the regions in the order used in the data
    Returns:
        seed_l_ind: index of left seed
        seed_r_ing: index of right seed
        
    '''
    seed_l_ind = ref_list.index(seed + "_L")
    seed_r_ind = ref_list.index(seed + "_R")
    return (seed_l_ind, seed_r_ind)
