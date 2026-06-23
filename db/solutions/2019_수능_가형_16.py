import sympy as sp
from sympy import symbols, ln, integrate, simplify

x = symbols('x', positive=True, real=True)
f = -sp.Rational(1,3) + 1/(3*x) + 2/(3*x**2)

# 원래 함수방정식 검증
lhs = 2*f + (1/x**2)*f.subs(x, 1/x)
rhs = 1/x + 1/x**2
verify_eq = simplify(lhs - rhs)
assert verify_eq == 0, f'Function equation failed: {verify_eq}'

# 적분 계산
result = integrate(f, (x, sp.Rational(1,2), 2))
result_simplified = simplify(result)

expected = 2*ln(2)/3 + sp.Rational(1,2)
assert simplify(result_simplified - expected) == 0, f'Integral mismatch: {result_simplified} vs {expected}'

print('VERIFY_PASS')