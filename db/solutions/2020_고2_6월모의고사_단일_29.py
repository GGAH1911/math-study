import math
from scipy.optimize import brentq
import numpy as np

CANDIDATE = 24

def f(x, k):
    arg = x - 7 + k
    if arg <= 0:
        return float('nan')
    return -2 * math.log2(arg) + 2

def equation(x, k):
    fval = f(x, k)
    return x**2 + fval**2 - 64

valid_k = []
for k in range(1, 40):
    left = max(-8.001, 7 - k + 0.001)
    right = 8
    if left >= right:
        continue
    
    roots = []
    x_vals = np.linspace(left, right, 200)
    y_vals = []
    
    for x in x_vals:
        try:
            y_vals.append(equation(x, k))
        except:
            y_vals.append(float('nan'))
    
    for i in range(len(x_vals) - 1):
        if not (np.isnan(y_vals[i]) or np.isnan(y_vals[i+1])):
            if y_vals[i] * y_vals[i+1] < 0:
                try:
                    root = brentq(equation, x_vals[i], x_vals[i+1], args=(k,))
                    is_dup = any(abs(root - r) < 1e-5 for r in roots)
                    if not is_dup:
                        roots.append(root)
                except:
                    pass
    
    if len(roots) >= 2:
        roots.sort()
        a, b = roots[0], roots[1]
        fa, fb = f(a, k), f(b, k)
        
        if a*b < 0 and fa*fb < 0:
            valid_k.append(k)

if valid_k:
    m, M = min(valid_k), max(valid_k)
    result = M + m
    if result == CANDIDATE:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')