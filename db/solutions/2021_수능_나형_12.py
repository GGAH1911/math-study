from sympy import symbols, summation, expand

n, k = symbols('n k', integer=True, positive=True)

# 일반항: a_n = n^2 - 3n + 3
def a(n_val):
    return n_val**2 - 3*n_val + 3

# 검증: sum_{k=1}^{n}(a_k - a_{k+1}) = -n^2 + n
for n_val in [1, 2, 3, 4, 5]:
    telescope_sum = sum(a(k_val) - a(k_val + 1) for k_val in range(1, n_val + 1))
    expected = -n_val**2 + n_val
    assert telescope_sum == expected, f'Mismatch at n={n_val}'

# a_1 = 1 확인
assert a(1) == 1, 'a_1 must equal 1'

# a_11 계산
result = a(11)
assert result == 91, f'Expected 91, got {result}'

print('VERIFY_PASS')