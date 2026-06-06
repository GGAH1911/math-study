import sympy as sp
x = sp.Symbol('x')

# 주어진 조건 (나): x³ - 10x + 13 - P(x) = {Q(x)}²
# 우리의 답: P(x) = x³ - 4x² + 6x - 3, Q(x) = 2x - 4

P = x**3 - 4*x**2 + 6*x - 3
Q = 2*x - 4

# 조건 (나) 검증
lhs = x**3 - 10*x + 13 - P
rhs = Q**2
verify_condition_b = sp.simplify(lhs - rhs)

# 조건 (가) 검증: P(x)Q(x)는 (x² - 3x + 3)(x - 1)로 나누어떨어짐
divisor = (x**2 - 3*x + 3) * (x - 1)
product = P * Q
quotient, remainder = sp.div(product, divisor)
verify_condition_a = remainder

# Q(0) < 0 검증
Q_at_0 = Q.subs(x, 0)
verify_Q0_negative = Q_at_0 < 0

# 최종 답
P_at_2 = P.subs(x, 2)
Q_at_8 = Q.subs(x, 8)
answer = P_at_2 + Q_at_8

if verify_condition_b == 0 and verify_condition_a == 0 and verify_Q0_negative and answer == 13:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')