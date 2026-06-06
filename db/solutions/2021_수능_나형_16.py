import sympy as sp
import numpy as np

x = sp.Symbol('x', real=True)
eqn = 4*sp.sin(x)**2 - 4*sp.cos(sp.pi/2 + x) - 3

# 원래 방정식으로 각 해 검증
solutions = [sp.pi/6, 5*sp.pi/6, 13*sp.pi/6, 17*sp.pi/6]
all_pass = True
for sol in solutions:
    val = eqn.subs(x, sol)
    val_simplified = sp.simplify(val)
    if abs(float(val_simplified)) > 1e-10:
        all_pass = False
        print(f'VERIFY_FAIL at x={sol}, eqn={val_simplified}')

if all_pass:
    total = sum(solutions)
    if sp.simplify(total - 6*sp.pi) == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')