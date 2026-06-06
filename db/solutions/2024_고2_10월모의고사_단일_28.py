import sympy as sp

# 구한 값
a1 = -14
d = 3
k = 7

# 조건 1 검증
term_sum = (a1 + (k-1)*d) + (a1 + k*d) + (a1 + (k+1)*d)
assert term_sum == 21, f'조건1 실패: {term_sum}'

# 조건 2 검증
S_k4 = sum(a1 + (n-1)*d for n in range(1, k+5))
assert S_k4 == 11, f'조건2 실패: {S_k4}'

# 답 계산
answer = a1 + (k+6-1)*d
assert answer == 22, f'답 계산 오류: {answer}'

print('VERIFY_PASS')