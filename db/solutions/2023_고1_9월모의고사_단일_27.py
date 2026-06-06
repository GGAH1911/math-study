import sympy as sp
x = sp.Symbol('x')
P = lambda x: 3*x + 1
Q = lambda x: x - 3

# 조건 1 검증: (x-2)P(x) - x^2 = (P(x)-x)Q(x) + (P(x)-3x)
lhs = (x-2)*P(x) - x**2
rhs = (P(x)-x)*Q(x) + (P(x)-3*x)
if sp.simplify(lhs - rhs) == 0:
    print('조건1 OK')
else:
    print('조건1 FAIL')

# 조건 2 검증: P(x)를 Q(x)로 나눈 나머지가 10
remainder = P(3)
if remainder == 10:
    print('조건2 OK')
else:
    print('조건2 FAIL')

# P(30) 계산
result = P(30)
if result == 91:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')