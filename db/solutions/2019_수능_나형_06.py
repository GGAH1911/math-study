from math import comb
import sympy as sp

x = sp.Symbol('x')
expanded = sp.expand((1 + x)**7)
coeff_x4 = expanded.coeff(x, 4)
print(f'Direct expansion coefficient of x^4: {coeff_x4}')

binom_result = comb(7, 4)
print(f'Binomial coefficient C(7,4): {binom_result}')

if coeff_x4 == 35 and binom_result == 35:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')