import sympy as sp

a = 4
x = sp.Symbol('x')

# 좌극한 계산 (x = -1)
left_limit = 2*(-1) + a

# 우극한 계산 (x = -1)
right_limit = (-1)**2 - 5*(-1) - a

# 함수값 (x = -1는 x <= -1 구간에 포함)
f_at_minus_one = 2*(-1) + a

# 모두 같은지 확인
if left_limit == right_limit == f_at_minus_one:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')