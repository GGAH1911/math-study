import numpy as np

def a(n):
    return 3 * n

def b(n):
    if n == 1:
        return 1.0
    return np.sqrt(n - 1)

# 조건식 검증: sum_{k=1}^{n} a_k * b_k^2 = n^3 - n + 3
for test_n in [1, 2, 3, 5, 10]:
    computed_sum = sum(a(k) * b(k)**2 for k in range(1, test_n + 1))
    expected = test_n**3 - test_n + 3
    assert np.isclose(computed_sum, expected), f'조건식 실패: n={test_n}'

# 극한값 검증
def f(n):
    return a(n) / (b(n) * b(2*n))

limit_approx = f(100000)
theoretical = 3 / np.sqrt(2)

if np.isclose(limit_approx, theoretical, rtol=1e-4):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')