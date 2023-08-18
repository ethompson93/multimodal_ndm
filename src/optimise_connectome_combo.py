'''runs GP-minimisation to optimise connectome combination for the network diffusion model'''

import numpy as np
import skopt
from src.ndm_combine_connectomes import ndm_combine_connectomes

def display_results(results, conns, search_params, data, seed):
    '''gives the parameters corresponding to the optimal connectome combination

        Parameters:
            results : results returned by the minimiser
            conns : the list of connectomes
            search_params : list of connectome names
            data : the target data array
            seed : the region used to initialise the model

        Returns:
            parameter dictionary with the weights assigned to each connectome
            and the Pearson's R correlation between the model output and the data
    '''

    # get the weights from the results
    best_params = np.asanyarray(results.x)
    weights = best_params/(np.sum(best_params))
    corr = ndm_combine_connectomes(conns, weights, data, seed)["r"]
    params = {}

    for i, conn in enumerate(search_params):
        print(conn, ": ", weights[i])
        params[conn] = weights[i]

    print ("r: ", corr )
    params["r"] = corr

    return params


def optimise_connectome_combo(conns, data, seed, n_calls, n_init):
    '''
    function to find the optimum connectome weights that minimise the difference 
    between the output of the network diffusion model and the measured data.

    Parameters:
        conns : list of connectomes to be included in the combined connectome
        data : array containing the target pathology data
        seed : seed region to initialise the model
        n_calls : number of calls to the Gaussian Process minimiser
        n_init : number of random initialisations for the GP minimiser

    Returns:
        best_params : dictionary with the weights assigned to each connectome, and 
                      the Pearson's R correlation between the model output and 
                      the data
        results : output from the GP-minimiser
    '''
    space = []
    for connectome in conns:
        space += [skopt.space.Real(0.00, 10, name=connectome.name, prior='uniform')]

    search_params = [connectome.name for connectome in conns]

    @skopt.utils.use_named_args(space)

    def objective(**params):
        weights = [params[connectome.name] for connectome in conns]
        return ndm_combine_connectomes(conns, weights, data, seed)["SSE"]

    results = skopt.gp_minimize(objective,
                                space,
                                n_calls=n_calls,
                                n_initial_points=n_init)

    best_params = display_results(results, conns, search_params, data, seed)

    return best_params, results
