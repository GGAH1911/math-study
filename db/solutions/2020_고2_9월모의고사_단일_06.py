import math
from sympy import symbols, solve, pi, sqrt

r = symbols('r', positive=True, real=True)
theta = pi / 4
area = 8 * pi

eq = (1/2) * r**2 * theta - area
solution = solve(eq, r)

if solution:
    r_val = float(solution[0])
    computed_area = 0.5 * r_val**2 * float(theta)
    expected_area = float(area)
    
    if abs(computed_area - expected_area) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')