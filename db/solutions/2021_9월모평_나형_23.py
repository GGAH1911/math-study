import sympy as sp

CANDIDATE = 8

x = sp.Symbol('x')

# f'(x) = -x^3 + 3
f_prime = -x**3 + 3

# f(x)를 적분으로 구함
f = sp.integrate(f_prime, x)

# 적분상수 C를 구하기 위해 f(2) = 10 조건 사용
# f(x) = -x^4/4 + 3x + C
# f(2) = -16/4 + 6 + C = -4 + 6 + C = 2 + C = 10
# 따라서 C = 8

C = 8
f_with_C = f + C

# f(2) = 10 검증
f_at_2 = f_with_C.subs(x, 2)
if f_at_2 != 10:
    print('VERIFY_FAIL')
else:
    # f(0) 계산
    f_at_0 = f_with_C.subs(x, 0)
    if f_at_0 == CANDIDATE:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')