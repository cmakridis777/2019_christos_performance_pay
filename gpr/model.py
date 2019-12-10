#======================================================================
#
#     sets the economic functions for the "Growth Model", i.e.,
#     the production function, the utility function
#
#
#     Simon Scheidegger, 11/16 ; 07/17
#======================================================================

import numpy as np

#======================================================================
#utility function u(c,l)


def utility(cons=[], lab=[], params=None):
    sum_util = 0.0
    n = len(cons)
    for i in range(n):
        nom1 = (cons[i] / params.big_A)**(1.0 - params.gamma) - 1.0
        den1 = 1.0 - params.gamma

        nom2 = (1.0 - params.psi) * ((lab[i]**(1.0 + params.eta)) - 1.0)
        den2 = 1.0 + params.eta

        sum_util += (nom1 / den1 - nom2 / den2)

    util = sum_util

    return util


#======================================================================
# output_f


def output_f(kap=[], lab=[], params=None):
    fun_val = params.big_A * (kap**params.psi) * (lab**(1.0 - params.psi))
    return fun_val


#======================================================================

# transformation to comp domain -- range of [k_bar, k_up]


def box_to_cube(knext=[]):
    n = len(knext)
    knext_box = knext[0:n]
    knext_dummy = knext[0:n]

    scaling_dept = (range_cube / (k_up - k_bar))  #scaling for kap

    #transformation onto cube [0,1]^d
    for i in range(n):
        #prevent values outside the box
        if knext[i] > k_up:
            knext_dummy[i] = k_up
        elif knext[i] < k_bar:
            knext_dummy[i] = k_bar
        else:
            knext_dummy[i] = knext[i]
        #transformation to sparse grid domain
        knext_box[i] = (knext_dummy[i] - k_bar) * scaling_dept

    return knext_box


#======================================================================