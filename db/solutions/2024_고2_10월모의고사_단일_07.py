import sympy as sp

# 문제의 조건
a, b = 2, -3

# x = 2에서 미분가능성 검증
# 좌미분
f_left = 2 - a
f_prime_left = 1

# 우미분
f_right = 4 + 2*b + a
f_prime_right = 4 + b

# 연속성 확인
if f_left == f_right:
    continuity_ok = True
else:
    continuity_ok = False

# 미분가능성 확인
if f_prime_left == f_prime_right:
    differentiable_ok = True
else:
    differentiable_ok = False

# f(2) 계산
f_2 = 2 - a

if continuity_ok and differentiable_ok and f_2 == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')