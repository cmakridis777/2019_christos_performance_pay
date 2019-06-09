import logging
logger = logging.getLogger(__name__)
import numpy as np
import math
from .stats import MultiDiscretizationLI


def solve(model):
    # Stores fitted value functions
    vfs = [None]*model.T

    # Define grid over continuous portion of state space
    z_grid = np.linspace(-10,10,10) # on a log scale, variance of noise is 0.06. If the process starts at 0, this range seems OK
    h_grid = np.linspace(0,30,10) # human capital, growth is upper bounded by 1 each time period.
    a_grid = np.exp(np.linspace(0,math.log(1.2e6),10))
    print(z_grid,h_grid,a_grid)




if __name__ == '__main__':
    pass