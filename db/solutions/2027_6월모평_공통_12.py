from fractions import Fraction
import sympy as sp

# 구한 값
a1 = 3
r = Fraction(1, 3)
a6 = a1 * (r ** 5)
product = a1 * a6

# 원래 조건 검증
a3 = a1 * (r ** 2)
cond1 = 2 * a1 * (a1 + a3)

a2 = a1 * r
cond2 = 5 * a2 * (a1 + a2)

print(f'a1={a1}, r={r}, a6={a6}')
print(f'Condition 1: 2*a1*(a1+a3) = {float(cond1)}')
print(f'Condition 2: 5*a2*(a1+a2) = {float(cond2)}')
print(f'a1 × a6 = {product}')

if float(cond1) == 20 and float(cond2) == 20 and product == Fraction(1, 27):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')