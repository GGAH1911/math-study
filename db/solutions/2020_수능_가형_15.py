from sympy import *
import math

# 검증: x_A = 1일 때
a1 = 3**(Rational(1,2))
x_a1 = 1
A1 = (x_a1, sqrt(3))
m_OA1 = sqrt(3) / x_a1
m_AB1 = (0 - sqrt(3)) / (4 - x_a1)
product1 = simplify(m_OA1 * m_AB1)

# 검증: x_A = 3일 때
a2 = 3**(Rational(1,6))
x_a2 = 3
A2 = (x_a2, sqrt(3))
m_OA2 = sqrt(3) / x_a2
m_AB2 = (0 - sqrt(3)) / (4 - x_a2)
product2 = simplify(m_OA2 * m_AB2)

# 모든 a의 곱
product_a = a1 * a2
result = simplify(product_a)

if product1 == -1 and product2 == -1 and result == 3**(Rational(2,3)):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')