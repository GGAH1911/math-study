import numpy as np

a = 7

def check_inequality_has_solution(a_val):
    x_vals = np.linspace(0, 2*np.pi - 0.001, 10000)
    inequality_vals = (2*a_val + 6)*np.cos(x_vals) - a_val*np.sin(x_vals)**2 + a_val + 12
    return np.any(inequality_vals < 0)

if check_inequality_has_solution(a):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')