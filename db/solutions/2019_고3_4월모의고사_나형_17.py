import sympy as sp
from sympy import sqrt, limit, oo, symbols

n = symbols('n', positive=True, integer=True)

a_n = sqrt(n**2 + 5*n + 4)
b_n = sqrt(n**2 + 2*n - 1)

diff = a_n - b_n

result = limit(12 / diff, n, oo)
print(f'Limit result: {result}')
print(f'Numerical check: {float(result)}')

if result == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')