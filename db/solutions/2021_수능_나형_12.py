from sympy import symbols, summation, simplify
n = symbols('n', integer=True, positive=True)
k = symbols('k', integer=True, positive=True)

# 일반항: a_n = n^2 - 3n + 3
def a(m):
    return m**2 - 3*m + 3

# a_1 = 1 확인
assert a(1) == 1, 'a_1 must be 1'

# 조건 검증: sum(a_k - a_{k+1}) = -n^2 + n
for test_n in range(1, 12):
    total = sum(a(i) - a(i+1) for i in range(1, test_n+1))
    expected = -test_n**2 + test_n
    assert total == expected, f'Condition fails at n={test_n}'

# a_11 계산
result = a(11)
assert result == 91, f'a_11 should be 91, got {result}'

print('VERIFY_PASS')