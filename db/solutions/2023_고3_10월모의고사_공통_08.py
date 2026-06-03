from sympy import symbols, diff, solve, Rational
x = symbols('x')
a_val = Rational(32, 3)
f = -x**4 - x**3 + 2*x**2
g = Rational(1, 3)*x**3 - 2*x**2 + a_val
h = g - f  # 원 문제: 모든 x에서 f(x) <= g(x) ↔ h(x) >= 0
h_prime = diff(h, x)
crits = solve(h_prime, x)
vals = [h.subs(x, c) for c in crits]
min_val = min(vals)
# a를 살짝 줄이면 어딘가에서 h<0 이 되어야 'a의 최솟값'이 맞음
a_less = a_val - Rational(1, 100)
h2 = Rational(1, 3)*x**3 - 2*x**2 + a_less - f
vals2 = [h2.subs(x, c) for c in crits]
min_val2 = min(vals2)
if min_val == 0 and min_val2 < 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
