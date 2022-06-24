import numpy as np
from system import avg_normal_params, full_ranges
from methods import shoot


LIN = 10 #lincpaces for ranges in bif_maps

def bifan(params, debug=False):
    
    bif_map = []
    n_params = len(params)
    for i, p in enumerate(params):
                        
        cnt, yt, D = shoot(0, 1, params=p)
        sgn = np.sign(D)
        bif_map.append(D)
        
        if debug:
            print(f'{i+1}/{n_params}   D = {D}')
    
    return bif_map



# def make_bifmaps(params, debug=False):
#     pass

# full_lins = []
# for i, dim in enumerate(full_ranges):
#     for j, ves in enumerate(dim):
#         full_lins.append(np.linspace(ves[0], ves[1], LIN))
        
# full_lins = np.array(full_lins).reshape((3, 5, LIN))
