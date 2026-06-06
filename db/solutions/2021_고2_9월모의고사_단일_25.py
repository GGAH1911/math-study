from sympy import symbols, simplify, Rational

# 검증: 주어진 조건들이 sum(a_n*b_n) = 23을 만족하는지
sum_a2 = 10
sum_ab = 23

# 조건 2 검증
cond2_left = 2 * sum_ab - 3 * sum_a2
print(f'조건2 좌변: {cond2_left}, 우변: 16')
assert cond2_left == 16, 'VERIFY_FAIL'

# 구하는 값 계산
answer = 6 * sum_a2 + 7 * sum_ab
print(f'sum a_n(6a_n + 7b_n) = 6*{sum_a2} + 7*{sum_ab} = {answer}')
assert answer == 221, 'VERIFY_FAIL'

print('VERIFY_PASS')