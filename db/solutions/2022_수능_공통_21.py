from sympy import symbols, simplify

# 수열 정의
a = [0] * 11  # a[0] unused, a[1]~a[10] used
a[1] = -2
a[2] = -4
a[3] = 8
a[4] = 16
a[5] = 32
a[6] = 64
a[7] = 128
a[8] = 256
a[9] = 512
a[10] = -1024

# 조건 (가) 검증
assert abs(a[1]) == 2, f'조건 (가) 실패: |a_1| = {abs(a[1])}'

# 조건 (나) 검증
for n in range(1, 10):
    expected = 2 * abs(a[n])
    actual = abs(a[n+1])
    assert actual == expected, f'조건 (나) 실패 n={n}: |a_{n+1}| = {actual}, 2|a_n| = {expected}'

# 조건 (다) 검증
total_sum = sum(a[1:11])
assert total_sum == -14, f'조건 (다) 실패: 합 = {total_sum}'

# 최종 답 검증
answer_sum = a[1] + a[3] + a[5] + a[7] + a[9]
assert answer_sum == 678, f'답 검증 실패: {answer_sum}'

print('VERIFY_PASS')