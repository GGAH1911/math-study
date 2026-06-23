from scipy.optimize import brentq
from numpy import pi, tan

def f(x):
    return tan(x) - x - pi/2

roots = []
for n in range(1, 11):
    lower = (n-1)*pi + 0.001
    upper = (n-1)*pi + pi/2 - 0.001
    try:
        root = brentq(f, lower, upper)
        roots.append(root)
    except:
        pass

if len(roots) < 6:
    print('VERIFY_FAIL')
else:
    # Check ㄱ: tan(a_n) = a_n + pi/2
    cond_a = all(abs(tan(roots[i]) - (roots[i] + pi/2)) < 1e-8 for i in range(5))
    
    # Check ㄴ: tan(a_{n+2}) - tan(a_n) > 2*pi
    cond_b = all(tan(roots[i+2]) - tan(roots[i]) > 2*pi - 1e-6 for i in range(len(roots)-2))
    
    # Check ㄷ: a_{n+1} + a_{n+2} > a_n + a_{n+3}
    cond_c = all(roots[i+1] + roots[i+2] > roots[i] + roots[i+3] for i in range(len(roots)-3))
    
    if cond_a and cond_b and cond_c:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')