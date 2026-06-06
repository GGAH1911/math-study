from sympy import symbols, expand, div, Poly

x = symbols('x')

# P(x)가 일반적인 일차식이라고 가정
# P(x) = ax + b
a, b = symbols('a b', real=True)

# P(x) = a*x + b
P = a*x + b

# P(x)를 (P(x) - 1)로 나눈 나머지
# P(x) = (P(x)-1)*q(x) + r(x)
# P(x) - (P(x)-1) = 1이므로
# P(x) = (P(x)-1)*1 + 1

# 검증: (P(x)-1) * 1 + 1 = P(x)
quotient = 1
remainder = 1
verification = (P - 1) * quotient + remainder
result = expand(verification - P)

if result == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')