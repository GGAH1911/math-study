import sympy as sp
x = sp.Symbol('x')

# 원래 다항식
P = x**4 + 2*x**3 + 11*x - 4

# 몫과 나머지
Q = x**2 - 3
R = 17*x + 5
divisor = x**2 + 2*x + 3

# 나눗셈 검증: P = divisor * Q + R
result = sp.expand(divisor * Q + R)

if result == P:
    # Q(2) + R(1) 계산
    Q_at_2 = Q.subs(x, 2)
    R_at_1 = R.subs(x, 1)
    answer = Q_at_2 + R_at_1
    
    # 검증
    if answer == 23:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')