import sympy as sp
a, b = -3, -3
# 연속성 검증: x=1에서 좌극한 = 우극한
left_limit = 3*1 + a
right_limit = 2*(1)**3 + b*1 + 1
assert left_limit == right_limit, f'연속성 실패: {left_limit} != {right_limit}'
# 미분가능성 검증: x=1에서 좌미분 = 우미분
f_prime_left = 3
f_prime_right = 6*(1)**2 + b
assert f_prime_left == f_prime_right, f'미분가능성 실패: {f_prime_left} != {f_prime_right}'
print('VERIFY_PASS')