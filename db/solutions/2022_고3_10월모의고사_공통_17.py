CANDIDATE = '15'

from sympy import symbols, solve

x, a, C = symbols('x a C')

# 문제 조건: 도함수 f'(x) = 3x^2 - 6x + a
f_prime = 3*x**2 - 6*x + a

# 극소 조건 f'(3) = 0에서 a 결정
condition_at_3 = f_prime.subs(x, 3)
# f'(3) = 3(9) - 6(3) + a = 27 - 18 + a = 9 + a = 0
a_value = solve(condition_at_3, a)[0]
assert a_value == -9, f'Expected a=-9, got {a_value}'

# 도함수 확정: f'(x) = 3x^2 - 6x - 9
f_prime_concrete = 3*x**2 - 6*x - 9

# 임계점 확인
critical_points = solve(f_prime_concrete, x)
assert set(critical_points) == {-1, 3}, f'Unexpected critical points: {critical_points}'

# 부호 분석을 통한 극대/극소 판정
test_left = f_prime_concrete.subs(x, -2)     # x < -1에서 부호
test_middle = f_prime_concrete.subs(x, 0)    # -1 < x < 3에서 부호
test_right = f_prime_concrete.subs(x, 4)     # x > 3에서 부호

assert test_left > 0, 'f\'(x) > 0 for x < -1'
assert test_middle < 0, 'f\'(x) < 0 for -1 < x < 3'
assert test_right > 0, 'f\'(x) > 0 for x > 3'

# x=-1에서 극대, x=3에서 극소 확인됨

# 원함수 구성: f'(x) 적분하면 f(x) = x^3 - 3x^2 - 9x + C
f = x**3 - 3*x**2 - 9*x + C

# 극댓값은 f(-1)이고, 이것이 CANDIDATE(15)와 같다는 조건
f_at_minus_1 = f.subs(x, -1)
# f(-1) = (-1)^3 - 3(-1)^2 - 9(-1) + C = -1 - 3 + 9 + C = 5 + C

candidate_value = int(CANDIDATE)
C_value = solve(f_at_minus_1 - candidate_value, C)[0]
assert C_value == 10, f'Expected C=10, got {C_value}'

# 최종 극댓값 계산
f_final = f.subs(C, C_value)
extreme_value = int(f_final.subs(x, -1))

# 검증: 극댓값이 CANDIDATE와 일치하는가?
if extreme_value == candidate_value:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')