import numpy as np
import scipy.optimize as opt

from solver import IPOptCallback
from . import bellman, dynamics
import utils.math as mu
from models import ModelDimensions

class DCSimple:
    def __init__(self, params):
        self.params = params
        self.dim = ModelDimensions(1,1,1)
        self.num_choices = 2

    # state-action value function
    def value(self, X, U, U_k = None, V_tp1=None, **kwargs):
        assert U_k is not None, "Must specify discrete action"
        V_tp1 = bellman.V_T if V_tp1 is None else V_tp1
        return bellman.state_action_value(X, U, U_k, self.params, V_tp1)

    def value_deriv(self, X, U, U_k = None, V_tp1=None, **kwargs):
        assert U_k is not None, "Must specify discrete action"
        V_tp1 = bellman.V_T if V_tp1 is None else V_tp1
        F = lambda U: bellman.state_action_value(X, U, U_k, self.params, V_tp1)
        # res = opt.approx_fprime(U,F,1e-8)
        res = mu.derivative_fd(F,U)
        return res

    @property
    def value_hess_sparsity(self):
        return mu.dense_hessian(self.dim.control)

    def constraints(self, X, U, **kwargs):
        return dynamics.EV_G(X, U, self.params)

    # returns derivative (jacobian) of constraint set
    def constraints_deriv(self, X, U, **kwargs):
        F = lambda U: dynamics.EV_G(X,U,self.params)
        return opt.approx_fprime(U,F,1e-8)

    @property
    def constraints_deriv_sparsity(self):
        return mu.dense_jacobian(self.dim.control, self.dim.constraints)

    @property
    def bounds_control(self):
        return dynamics.control_bounds(self.params)

    @property
    def bounds_constraint(self):
        return dynamics.constraint_bounds(self.params)
