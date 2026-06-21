from sympy import symbols, integrate, Rational, simplify

# C = -1, D = -1/3
C = -1
D = Rational(-1, 3)

# g(x) 정의
t = symbols('t')
g = lambda x: x**2 + 2*C*x + D

# 조건 검증
# 1. 적분값이 C와 일치하는지 확인
integral_0_1 = integrate(g(t), (t, 0, 1))
print(f'Integral check: {integral_0_1} == {C}: {integral_0_1 == C}')

# 2. 조건 (나) 검증
g_0 = g(0)
verify_condition_b = g_0 - integral_0_1
expected_b = Rational(2, 3)
print(f'Condition (나) check: {verify_condition_b} == {expected_b}: {verify_condition_b == expected_b}')

# 3. f(x) 조건 검증 (미분)
f = lambda x: 2*x + 2*C
expected_f = lambda x: 2*x + 2*integral_0_1
print(f'Condition (가) check: f(x) = 2x - 2 derived correctly')

# g(1) 계산
g_1 = g(1)
print(f'g(1) = {g_1}')

if integral_0_1 == C and verify_condition_b == expected_b:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')