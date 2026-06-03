import math

# n의 범위 확인: 4 < n < 10
valid_n = [5, 6, 7, 8, 9]

for n in valid_n:
    # 교점의 x좌표
    x = (-3 + math.sqrt(9 + 4*n)) / 2
    # 1 < x < 2인지 확인
    assert 1 < x < 2, f"n={n}: x={x} is not in (1, 2)"
    # 원래 방정식 x^2 + 3x = n 검증
    assert abs(x**2 + 3*x - n) < 1e-10, f"n={n}: x^2+3x != n"

# 경계값 확인
x_at_4 = (-3 + math.sqrt(9 + 16)) / 2  # n=4일 때 x=1
assert x_at_4 == 1.0
x_at_10 = (-3 + math.sqrt(9 + 40)) / 2  # n=10일 때 x=2
assert x_at_10 == 2.0

result_sum = sum(valid_n)
assert result_sum == 35
print('VERIFY_PASS')