from itertools import product

# 전체 문자열 생성
letters = ['a', 'b', 'c', 'd']
all_strings = [''.join(p) for p in product(letters, repeat=4)]

# 조건 확인 함수
def count_char(s, c):
    return s.count(c)

# A: a가 정확히 1개
A = [s for s in all_strings if count_char(s, 'a') == 1]

# B: b가 정확히 1개
B = [s for s in all_strings if count_char(s, 'b') == 1]

# A ∪ B
A_union_B = set(A) | set(B)

# 확률 계산
prob_num = len(A_union_B)
prob_den = len(all_strings)

# 기약분수로 변환
from math import gcd
g = gcd(prob_num, prob_den)
result_num = prob_num // g
result_den = prob_den // g

# 검증: 21/32 = 168/256
if result_num == 21 and result_den == 32:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result_num}/{result_den}, expected 21/32')