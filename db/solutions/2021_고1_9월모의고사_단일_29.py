from sympy import symbols, expand

x = symbols('x')

# 이미지에서 주어진 원래 조건
Q = x**3 - 3*x**2 + 2*x
P = 2*x**4 - 4*x**3 + 7*x**2 - 5*x

# 원래 주어진 함수방정식 검증
LHS = (Q.subs(x, x+1))**2 + Q**2
RHS = (x**2 - x) * P

LHS_simplified = expand(LHS)
RHS_simplified = expand(RHS)

# 조건 만족 확인
condition_check = LHS_simplified - RHS_simplified

if expand(condition_check) == 0:
    # 나머지 계산
    R = 9*x**2 - 9*x
    R_at_3 = R.subs(x, 3)
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')