# 원래 문제 조건 검증
a = 15
d = 4

# 조건 1: 모든 항이 자연수인지 확인
for n in range(1, 8):
    a_n = a + (n-1)*d
    assert a_n >= 1, f'a_{n} = {a_n} is not natural'

# 조건 2: a_7이 13의 배수
a_7 = a + 6*d
assert a_7 % 13 == 0, f'a_7 = {a_7} is not divisible by 13'

# 조건 3: 합 조건
sum_S = 0
for k in range(1, 8):
    S_k = (k/2) * (2*a + (k-1)*d)
    sum_S += S_k

assert abs(sum_S - 644) < 1e-9, f'Sum S_k = {sum_S}, expected 644'

# 최종 답
a_2 = a + d
assert a_2 == 19, f'a_2 = {a_2}, expected 19'

print('VERIFY_PASS')