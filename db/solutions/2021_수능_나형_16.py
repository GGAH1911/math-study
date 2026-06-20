import sympy as sp
x = sp.Symbol('x', real=True)
expr = 4*sp.sin(x)**2 - 4*sp.cos(sp.pi/2 + x) - 3
sols = sp.solveset(expr, x, domain=sp.Interval(0, 4*sp.pi, False, True))
sols_list = list(sols)
total = sp.simplify(sum(sols_list))
print('Solutions:', sorted([sp.simplify(s) for s in sols_list]))
print('Sum:', total)
if sp.simplify(total - 6*sp.pi) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')