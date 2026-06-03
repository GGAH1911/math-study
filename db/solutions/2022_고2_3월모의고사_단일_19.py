from sympy import symbols, divisors, symbols

# 주어진 값
k = 9
m = 6
U = set(range(1, k + 1))

# A: m의 약수
A = set(divisors(m)) & U

# B 구성
B = {1, 4, 7}

# 검증
assert B - A == {4, 7}, f'(가) B - A 검증 실패: {B - A}'
A_union_B_complement = A | (U - B)
assert len(A_union_B_complement) == 7, f'(가) n(A∪B^C) 검증 실패: {len(A_union_B_complement)}'
assert sum(A) == sum(B), f'(나) sum 검증 실패: sum(A)={sum(A)}, sum(B)={sum(B)}'

# 답 계산
A_complement = U - A
B_complement = U - B
result_set = A_complement & B_complement
answer_value = sum(result_set)

assert answer_value == 22, f'최종 답 검증 실패: {answer_value}'
print('VERIFY_PASS')