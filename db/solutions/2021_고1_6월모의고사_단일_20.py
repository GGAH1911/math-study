import sympy as sp
from sympy import sqrt, simplify, expand

x = (1 + sqrt(5)) / 2

result = 1 - x + x**2 - x**3 + x**4 - x**5 + x**6 - x**7 + x**8
result_simplified = simplify(expand(result))

p_val = 16
q_val = 6
expected = p_val + q_val * sqrt(5)

if simplify(result_simplified - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Result: {result_simplified}')
    print(f'Expected: {expected}')