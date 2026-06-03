from sympy import symbols, solve, Rational
x = symbols('x')
P = set(solve((x+1)*(x+2)*(x-3), x))
valid_ks = []
for k in range(-50, 51):
    Q = set(solve(x**2 + k*x + k - 1, x))
    if Q.issubset(P) and len(Q) >= 1:
        valid_ks.append(k)
prod = 1
for k in valid_ks:
    prod *= k
print('valid_ks=', valid_ks, 'product=', prod)
print('VERIFY_PASS' if prod == -12 else 'VERIFY_FAIL')
