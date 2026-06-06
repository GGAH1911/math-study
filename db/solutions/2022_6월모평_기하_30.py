import numpy as np
from scipy.optimize import fminbound

R = np.array([4, 4])

def verify():
    # Case 2-1: P on AB, Q = A(2,0) — should give min = 16
    P_min = np.array([0, 2])  # B
    Q = np.array([2, 0])      # A
    RP = P_min - R
    RQ = Q - R
    result = np.dot(RP, RQ)
    assert result == 16, f'Case 2-1 min failed: {result}'
    
    # Case 1-1: P = A(2,0), Q = D(0,-2) — should give max = 32
    P = np.array([2, 0])
    Q = np.array([0, -2])
    RP = P - R
    RQ = Q - R
    result = np.dot(RP, RQ)
    assert result == 32, f'Case 1-1 max failed: {result}'
    
    # Case 1-2: P = (1,1), Q = (-1,-1) — should give 30
    P = np.array([1, 1])
    Q = np.array([-1, -1])
    RP = P - R
    RQ = Q - R
    result = np.dot(RP, RQ)
    assert result == 30, f'Case 1-2 failed: {result}'
    
    # Case 2-2: P = (0,-0) on BC, Q = (1,-1) — should give 32
    P = np.array([0, 0])
    Q = np.array([1, -1])
    RP = P - R
    RQ = Q - R
    result = np.dot(RP, RQ)
    assert result == 32, f'Case 2-2 max failed: {result}'
    
    print('VERIFY_PASS')

verify()