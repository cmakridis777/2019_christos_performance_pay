#======================================================================
#
#     This routine interfaces with Gaussian Process Regression
#     The crucial part is
#
#     y[iI] = solver.initial(Xtraining[iI], n_agents)[0]
#     => at every training point, we solve an optimization problem
#
#     Simon Scheidegger, 01/19
#======================================================================

import numpy as np
# from parameters import *
from . import nonlinear_solver_initial as solver
import pickle

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, Matern

#======================================================================


def GPR_init(iteration, params):

    print("hello from step ", iteration)

    #fix seed
    np.random.seed(666)

    #generate sample aPoints
    dim = params.n_agents
    Xtraining = np.random.uniform(params.k_bar, params.k_up,
                                  (params.No_samples, dim))
    y = np.zeros(params.No_samples, float)  # training targets

    # solve bellman equations at training points
    for iI in range(len(Xtraining)):
        y[iI] = solver.initial(Xtraining[iI], params.n_agents, params)[0]

    #for iI in range(len(Xtraining)):
    #print Xtraining[iI], y[iI]

    # Instantiate a Gaussian Process model
    kernel = RBF()

    #kernel = 1.0 * RBF(length_scale=1.0, length_scale_bounds=(1e-1, 10.0))
    #kernel = 1.0 * Matern(length_scale=1.0, length_scale_bounds=(1e-1, 10.0),nu=1.5)

    #kernel = 1.0 * RBF(length_scale=100.0, length_scale_bounds=(1e-1, 2e2)) \
    #+ WhiteKernel(noise_level=1, noise_level_bounds=(1e-3, 1e+0))

    gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9)

    # Fit to data using Maximum Likelihood Estimation of the parameters
    gp.fit(Xtraining, y)

    #save the model to a file
    output_file = params.filename + str(iteration) + ".pcl"
    print(output_file)
    with open(output_file, 'wb') as fd:
        pickle.dump(gp, fd, protocol=pickle.HIGHEST_PROTOCOL)
        print("data of step ", iteration, "  written to disk")
        print(" -------------------------------------------")
    fd.close()


#======================================================================