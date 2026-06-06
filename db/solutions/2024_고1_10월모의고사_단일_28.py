import sympy as sp
x = sp.Symbol('x')
P = sp.Rational(17,8)*x**2 - sp.Rational(9,4)*x
Q = sp.Rational(15,8)*x**2 - sp.Rational(7,4)*x

# 조건 (가) 검증
lhs = P**2 - Q**2
rhs = x**2*(x-1)*(x-2)
if sp.expand(lhs - rhs) == 0:
    print('Condition (가): VERIFY_PASS')
else:
    print('VERIFY_FAIL')

# 조건 (나) 검증
val_P2_minus_Q2 = abs(float(P.subs(x, 2) - Q.subs(x, 2)))
val_P1_minus_Q1 = abs(float(P.subs(x, 1) - Q.subs(x, 1)))
if val_P2_minus_Q2 < val_P1_minus_Q1:
    print('Condition (나): VERIFY_PASS')
else:
    print('VERIFY_FAIL')

# P(3) + Q(3) = 24 검증
if P.subs(x, 3) + Q.subs(x, 3) == 24:
    print('P(3)+Q(3)=24: VERIFY_PASS')
else:
    print('VERIFY_FAIL')

# P(4) 계산
result = P.subs(x, 4)
if result == 25:
    print('P(4)=25: VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: P(4)={result}')