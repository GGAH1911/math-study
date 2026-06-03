import sympy as sp

# 수열 정의
def a_n(n):
    if n == 1:
        return 1
    else:
        return -1 / (n * (n - 1))

# S_n = 1/n 검증
for n in range(1, 8):
    S_n = sum(a_n(k) for k in range(1, n + 1))
    expected = 1 / n
    assert abs(S_n - expected) < 1e-10, f"S_{n} verification failed"

# 구하는 값 계산
result = a_n(1)
for k in range(2, 8):
    result += 1 / ((k - 1) * a_n(k))

if abs(result - (-26)) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')