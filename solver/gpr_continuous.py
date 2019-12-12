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
import logging
import sys
logger = logging.getLogger(__name__)
logger.write = lambda msg: logger.info(msg.decode('utf-8')) if msg.strip(
) != '' else None
import pickle

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, Matern

from . import nonlinear_solver as solver
from utils import stdout_redirector


def GPR_iter(model, iteration, checkpoint_out, checkpoint_in=None):
    logger.info("Beginning Step %d" % iteration)

    # Load checkpoint from disk
    gp_old = None
    if checkpoint_in is not None:
        with open(checkpoint_in, 'rb') as fd_old:
            gp_old = pickle.load(fd_old)
            logger.info('Data from iteration step %d loaded from disk' %
                        (iteration - 1))

    #fix seed
    np.random.seed(666)

    #generate sample aPoints
    dim = model.params.n_agents
    Xtraining = np.random.uniform(model.params.k_bar, model.params.k_up,
                                  (model.params.No_samples, dim))
    y = np.zeros(model.params.No_samples, float)  # training targets

    # solve bellman equations at training points
    # with stdout_redirector(logger):
    for iI in range(len(Xtraining)):
        y[iI] = solver.solve(model, Xtraining[iI], gp_old)[0]

    # Instantiate a Gaussian Process model
    # Fit to data using Maximum Likelihood Estimation of the parameters
    kernel = RBF()
    gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9)
    gp.fit(Xtraining, y)

    #save the model to a file
    logger.info('Output file: %s' % checkpoint_out)
    with open(checkpoint_out, 'wb') as fd:
        pickle.dump(gp, fd, protocol=pickle.HIGHEST_PROTOCOL)
        logger.info("Step %d data  written to disk" % iteration)