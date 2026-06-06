import sympy as sp

# 수열 일반항
def a(n):
    if n % 2 == 1:  # 홀수
        return 10 - n - 1
    else:  # 짝수
        return 7 + n

# a_1 = 10 - 2 = 8
# a_2 = 7 + 2 = 9
# a_3 = 10 - 4 = 6
# a_4 = 7 + 4 = 11

assert a(1) == 8
assert a(2) == 9
assert a(3) == 6
assert a(4) == 11
assert a(5) == 4
assert a(6) == 13

# 조건 (가) 확인: 첫 2n개 합 = 17n
for n in range(1, 6):
    s = sum(a(k) for k in range(1, 2*n + 1))
    assert s == 17*n, f"n={n}: {s} != {17*n}"

# 조건 (나) 확인: |a_{n+1} - a_n| = 2n - 1
for n in range(1, 20):
    diff = abs(a(n+1) - a(n))
    expected = 2*n - 1
    assert diff == expected, f"n={n}: {diff} != {expected}"

# 답 검증
result = sum(a(2*n) for n in range(1, 11))
assert result == 180
print('VERIFY_PASS')