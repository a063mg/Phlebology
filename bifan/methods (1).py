import numpy as np
from numpy.linalg import det, inv, svd, norm
from system import full_system, avg_normal_params, Graph



def error(left, right, 
          params=avg_normal_params, 
          ro=1.05,
          heart_p=5, 
          debug=False):
    """
    1. Mass conservation
    2. Momentum conservation
    """
    Res, Sq, Ext = params
    left = left.reshape((len(Graph), -1))
    right = right.reshape((len(Graph), -1))
    err = []
        
    for i, ves in enumerate(Graph):
        V_i = right[i][0]
        Q_i = right[i][1] 
        moment_i = Q_i**2 / 2 / Sq[i]**2 + V_i / Ext[i] / ro
        
        if debug:
            print(f'Vessel {i}: V{i} = {V_i}, Q{i} = {Q_i}')
            print(f'Momentum = {moment_i}')
        
        if i == len(Graph) - 1:
            moment_i -= heart_p
        
        for to in ves:
            
            V_to = left[to][0]
            Q_to = left[to][1]
            moment_to = Q_to**2 / 2 / Sq[to]**2 + V_to / Ext[to] / ro
            
            if debug:
                print(f'\t to vessel: V{to} = {V_to}, Q{to} = {Q_to}, Sqto = {Sq[to]}, Extto = {Ext[to]}')
                print(f'\t \t mass = {V_to} \t moment = {moment_to}')
            
            # mass
            V_i -= V_to
            
            # momentum
            moment_i -= moment_to
        
            if debug:
                print(f'\t Junction: {i} -> {to}: mass = {V_i} \t momentum = {moment_i}')
        
        err += [V_i, moment_i]
    
    return np.array(err)


def RK_system(t0, t1, y_init, 
              system = full_system, 
              params = avg_normal_params,
              n = 100):
    """
    y0 = V(t0) = V0, Q(t0) = Q0
    """
    
    y0 = y_init.copy()
    h = (t1 - t0) / n
    
    for i in range(n):
        k1 = system(t0, y0, params)
        k2 = system(t0 + h/2, y0 + k1 * h/2, params)
        k3 = system(t0 + h/2, y0 + k2 * h/2, params)
        k4 = system(t0 + h, y0 + k3 * h, params)
        k = h * (k1 + 2*k2 + 2*k3 + k4) / 6
        
        t0 += h
        y0 += k
        
    return y0



def shoot(t0, t1, 
          y_init = np.ones(len(Graph)*2),
          system = full_system,
          params = avg_normal_params,
          solver = RK_system,
          error = error,
          eps = 10**(-4),
          delta = 10**(-5),
          debug = False):

    t = (t1 - t0) / 2
    yt = y_init.astype(np.float32)
    
    cnt = 0
    D = np.nan
    while True:
        cnt += 1
        # print(f'Iteration: {cnt}')
        left = solver(t, t0, yt, system, params)
        right = solver(t, t1, yt, system, params)
        err = error(left, right, params)
        
        # print(f'yt = {yt}\t Boundaries: {left}\t{right}\tError: {err}')
        
        # Converged
        if (abs(err) < delta).all():
#             if debug:
            print(f'Converged in {cnt} iterations ', end='')
                
            break
        
        # find Jacobian and its determinant
        J = np.empty((len(err), len(yt)))
        for i in range(len(yt)):

            yi = yt.copy()
            yi[i] += eps
            left = solver(t, t0, yi, system, params)
            right = solver(t, t1, yi, system, params)
            erri = error(left, right, params)
            # print(f'\t Changing yt\t y{i} : {yi}\t Boundaries: {left}\t{right}\tError: {erri}')
            
            J[:, i] = (erri - err) / eps

        # print(f'\t Jacobian: {J.flatten()}')
        
        D = det(J)
        try:
            print(f'Error norm: {np.norm(err)}')
            u, s, vh = np.linalg.svd(J)
            print(f'Singular vales: {s}')
        except:
            pass
        
        
        # Critical point
        if abs(D) < 10**(-10):
            if debug:
                print(f'Critical point found in {cnt} iterations | Error = {np.round(err, 3)}')
            break
        
        # Update yt and calculate new error
        yt -= np.dot(np.linalg.inv(J),  err)
    
        # Iteration limit exceeded
        if cnt == 30:
            D = np.nan
            break

        if debug:
            print(cnt, D)
            
    if D:
        D = round(D, 5)
    return cnt, yt, D



