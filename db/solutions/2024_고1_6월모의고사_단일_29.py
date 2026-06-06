import numpy as np
from scipy.optimize import fminbound

def S(x):
    return (4 + 2*x - x**2) / 8

def verify_max():
    # Find maximum of S(x) on (0, sqrt(2))
    max_x = fminbound(lambda x: -S(x), 0.01, np.sqrt(2) - 0.01)
    max_val = S(max_x)
    
    # Check x = 1
    s_at_1 = S(1.0)
    
    # Verify it equals 5/8
    expected = 5/8
    
    if abs(s_at_1 - expected) < 1e-10 and abs(max_val - expected) < 1e-10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')

verify_max()