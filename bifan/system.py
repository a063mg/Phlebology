import numpy as np


"""
Citrculatory system graph
element index - from-vessel
element - array of to-vessels
"""
Graph = np.array([[1], [2], [3], [4], [0]])
N_vessels = len(Graph)


"""
Average normal parameters 
axis_0 - Res, Sq, Ext
axis_1 - vessel number
"""
avg_normal_params = np.array([[70, 125, 125, 20.25, 20.25],
                              [510.55, 98.15, 631.85, 166.9, 166.9], 
                              [0.0215, 0.07, 0.06, 0.15, 0.27]])


"""
axis_0 - Res, Sq, Ext
axis_1 - vessel number
axis_2 - [min_patalogy, max_patalogy] 
"""

full_ranges = np.array([[[30, 100], [30, 210], [30, 210], [0, 150], [0, 150]], 
                        [[78.5, 1590.4], [0.5, 491], [0.5, 3849], [0.5, 1257], [0, 1591]],
                        [[0.0001, 0.1], [0.0001, 0.5], [0.0001, 0.5], [0.0001, 0.6], [0.0001, 0.6]]])



LIN = 10
full_lins = []

for i, dim in enumerate(full_ranges):
    for j, ves in enumerate(dim):
        full_lins.append(np.linspace(ves[0], ves[1], LIN))
        
full_lins = np.array(full_lins).reshape((3, len(Graph), LIN))


##########################
Graph = Graph[[0, 4]]

As = [0, 8]
Bs = [8, 21]
avg_normal_params = np.array([[0.002, 0.002],
                              [350, 160], 
                              [0.32, 0.22]]) 
full_ranges = np.array([[[0.0005, 0.05], [0.0005, 0.05]],
                        [[200, 400], [100, 300]],
                        [[0, 0.4], [0, 0.3]]])

full_lins = []

for i, dim in enumerate(full_ranges):
    for j, ves in enumerate(dim):
        full_lins.append(np.linspace(ves[0], ves[1], LIN))
full_lins = np.array(full_lins).reshape((3, len(Graph), LIN))
##########################



"""
Physical Equations
"""
def dV(Q, a, b):
    return Q / (b - a)


def dQ(V, Q, a, b, R=10, I=0.0003, C=10):
    return -Q * R / I / (b - a) - V / I / C


def system_i(t, var, i, Res, Ext):
    V, Q = var
    R, I, C = Res[i], 0.1, Ext[i]
    a, b = As[i], Bs[i]
    return np.array([dV(Q, a, b), dQ(V, Q, a, b, R, I, C)])


def full_system(t, var, params=avg_normal_params):
    Res, Sq, Ext = params
    res = []
    for i in range(0, len(var), 2):
        v = var[i:i+2]
        res.append(system_i(t, v, i // 2, Res, Ext))
        
    return np.array(res).flatten()