CANDIDATE = 21

from sympy import symbols, simplify, Rational

# a를 구하기 위해 최댓값 조건 이용
# (1/3)^(4-a) = 27
# 3^(-(4-a)) = 3^3
# -(4-a) = 3
# a = 7
a = 7

# 최댓값 검증: x=2일 때
f_max = (Rational(1, 3)) ** (2*2 - a)
print(f'f(2) = (1/3)^(4-{a}) = {f_max}')
assert f_max == 27, f'최댓값이 27이 아님: {f_max}'

# 최솟값 계산: x=3일 때
m = (Rational(1, 3)) ** (2*3 - a)
print(f'f(3) = (1/3)^(6-{a}) = {m}')

# a × m 계산
result = a * m
print(f'a × m = {a} × {m} = {result}')

if result == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')