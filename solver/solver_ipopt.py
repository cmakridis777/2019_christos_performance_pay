# Nonlinear Solver:
#   Uses nonlinear optimization library to optimize the
#   RHS of the Bellman equation

import logging
logger = logging.getLogger(__name__)
import numpy as np
import ipyopt


def solve(model, X, **kwargs):

    tol = 1e-6 if 'tol' not in kwargs else kwargs['tol']
    acceptable_tol = 1e-5 if 'acceptable_tol' not in kwargs else kwargs['acceptable_tol']

    # IPOPT PARAMETERS below
    N = model.dim.control
    M = model.dim.constraints

    U_L, U_U = model.bounds_control
    U = 0.5*(U_U - U_L) + U_L
    G_L, G_U = model.bounds_constraint

    # Create callback functions
    def eval_f(U):
        out = model.value(X, U, **kwargs)
        return out

    def eval_grad_f(U, out):
        out[()] = model.value_deriv(X, U, **kwargs)
        return out

    def eval_g(U, out):
        out[()] = model.constraints(X, U, **kwargs)
        return out

    def eval_jac_g(U, out):
        out[()] = model.constraints_deriv(X, U, **kwargs)
        return out

    ipyopt.set_loglevel(ipyopt.LOGGING_DEBUG)

    # First create a handle for the Ipopt problem
    nlp = ipyopt.Problem(N, U_L, U_U, M, G_L, G_U,
                         model.constraints_deriv_sparsity,
                         model.value_hess_sparsity, eval_f, eval_grad_f,
                         eval_g, eval_jac_g)

    nlp.set(obj_scaling_factor=-1.00,
            tol=tol,
            acceptable_tol=acceptable_tol,
            derivative_test='first-order',
            hessian_approximation="limited-memory",
            print_level=0)

    z_l = np.zeros(N)
    z_u = np.zeros(N)
    constraint_multipliers = np.zeros(M)
    u, obj, status = nlp.solve(U,
                               mult_g=constraint_multipliers,
                               mult_x_L=z_l,
                               mult_x_U=z_u)

    return obj, u, status