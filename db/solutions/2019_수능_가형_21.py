from sympy import *
x_sym = symbols('x', real=True)
C_val = Rational(8, 3)
f_neg1_cubed = C_val / 3
f_neg1 = f_neg1_cubed ** (Rational(1, 3))
f_neg1_simplified = simplify(f_neg1)
result = nsimplify(f_neg1_simplified, rational=False)
print(f'f(-1)^3 = {f_neg1_cubed}')
print(f'f(-1) = {result}')
expected = 2 * 3**(Rational(1,3)) / 3
verify = simplify(result - expected) == 0
print('VERIFY_PASS' if verify else f'VERIFY_FAIL: {result} != {expected}')