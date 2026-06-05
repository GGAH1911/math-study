import sympy as sp
t = sp.Symbol('t', positive=True)
# e^f(t) = t / (e^(2t) - e^(-3t))  (원래 조건에서 직접 유도)
expr = t / (sp.exp(2*t) - sp.exp(-3*t))
limit_val = sp.limit(expr, t, 0, '+')
expected = sp.Rational(1, 5)
if limit_val == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {limit_val}, expected {expected}')