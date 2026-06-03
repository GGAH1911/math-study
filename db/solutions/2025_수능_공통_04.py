import sympy as sp

a = 7

# 좌극한 계산
left_limit = 5 * (-2) + a

# 우극한 계산
right_limit = (-2)**2 - a

# 함숫값 (x = -2에서 x >= -2 구간 적용)
f_at_minus2 = (-2)**2 - a

# 연속 조건 확인
if left_limit == right_limit == f_at_minus2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')