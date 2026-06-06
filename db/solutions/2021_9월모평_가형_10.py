import sympy as sp

# 점화식에서 수열 항 계산
a = {1: 12}
for n in range(1, 9):
    coeff = (-1)**(n+1) * n
    a[n+1] = coeff - a[n]

# a_8 > a_1 검증
assert a[8] > a[1], f"a_8={a[8]} should be > a_1={a[1]}"

# 8보다 작은 k에서는 조건 불만족 확인
for k in range(2, 8):
    assert a[k] <= a[1], f"Found smaller k={k} with a[k]={a[k]} > a[1]={a[1]}"

# 점화식 검증
for n in range(1, 8):
    expected = (-1)**(n+1) * n
    actual = a[n+1] + a[n]
    assert actual == expected, f"점화식 오류: n={n}, {actual} != {expected}"

print('VERIFY_PASS')