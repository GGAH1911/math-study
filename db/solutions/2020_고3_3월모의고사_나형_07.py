import numpy as np
from scipy.optimize import fsolve

def equation(x):
    return np.cos(2*x) - np.sin(4*x)

solutions = []
for start in np.linspace(0, 2*np.pi, 100):
    sol = fsolve(equation, start, full_output=True)
    if sol[2] == 1:  # 수렴 성공
        x_sol = sol[0][0]
        if 0 <= x_sol <= 2*np.pi:
            is_new = True
            for existing in solutions:
                if np.isclose(x_sol, existing, atol=1e-6):
                    is_new = False
                    break
            if is_new:
                solutions.append(x_sol)

solutions.sort()
count = len(solutions)

if count == 8:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: found {count} solutions instead of 8')