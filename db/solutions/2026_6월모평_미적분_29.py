import sympy as sp
from fractions import Fraction

# α = -1, β = -2
alpha, beta = -1, -2

# 검증: a1*a2*a3*a4 = 4
a1, a2, a3, a4 = alpha, -beta, -alpha, beta
product = a1 * a2 * a3 * a4
assert product == 4, f'Product check failed: {product}'

# 공비 r = -2/3, b1 = 5
r = Fraction(-2, 3)
b1 = 5

# 첫 번째 조건: a2 * b1 / (1-r) = 6
sum1 = a2 * b1 / (1 - r)
assert sum1 == 6, f'Sum1 check failed: {sum1}'

# 두 번째 조건: a1 * b1 * r / (1-r^2) = 6
sum2 = a1 * b1 * r / (1 - r**2)
assert sum2 == 6, f'Sum2 check failed: {sum2}'

# b1 * b3 계산
b3 = b1 * r**2
product_b = b1 * b3
assert product_b == Fraction(100, 9), f'b1*b3 check failed: {product_b}'

# p + q
p, q = 9, 100
assert sp.gcd(p, q) == 1, 'Not coprime'
result = p + q
assert result == 109, f'Final answer check failed: {result}'

print('VERIFY_PASS')