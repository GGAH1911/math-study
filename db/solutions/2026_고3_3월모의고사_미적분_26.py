from sympy import Rational, limit, oo, symbols, simplify
n, a = symbols('n a', positive=True, integer=True)

def compute_limit(a_val):
    expr = (5*a_val**(2*n) + (2*a_val)**(n+1)) / (a_val**(2*n) + (2*a_val)**n)
    return limit(expr, n, oo)

valid = []
for a_val in range(1, 30):
    L = compute_limit(a_val)
    if L == a_val + 1:
        valid.append(a_val)

total = sum(valid)
print('valid a =', valid, 'sum =', total)
if total == 5 and set(valid) == {1, 4}:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
