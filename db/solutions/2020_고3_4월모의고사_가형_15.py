from sympy import *
a1 = Rational(1, 9)
b1 = 36 * a1
print(f'b1 = {b1}')

# 무한급수 검증
a = symbols('n', integer=True, positive=True)
sum_val = b1 / (3 * a1)
print(f'Sum = {sum_val}')
if sum_val == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')