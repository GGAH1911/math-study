from sympy import symbols, solve, summation

# 검증: 주어진 원래 조건들을 만족하는 수열들의 예
# a_k들의 합이 5, b_k들의 합이 15인 경우를 확인

sum_a = 5
sum_b = 15

# 조건 1 검증: sum(2*a_k + 3) = 40
result1 = 2 * sum_a + 3 * 10
assert result1 == 40, f'조건1 실패: {result1}'

# 조건 2 검증: sum(a_k - b_k) = -10
result2 = sum_a - sum_b
assert result2 == -10, f'조건2 실패: {result2}'

# 구하는 값: sum(b_k + 5)
answer = sum_b + 5 * 10
assert answer == 65, f'답 검증 실패: {answer}'

print('VERIFY_PASS')