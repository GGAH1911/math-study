from sympy import symbols, summation

a1, n, m = symbols('a1 n m', integer=True)
d = 5
a_n = lambda k: -72 + (k - 1) * 5

# 검증: a_21
a_21 = a_n(21)
assert 24 < a_21 < 29, f"a_21={a_21} 범위 오류"

# 검증: 조건 (가)
sum_29 = sum(a_n(k) for k in range(1, 30))
assert sum_29 < 0, f"조건(가) 실패: {sum_29}"

# 검증: 조건 (나)
m_val = 14
sum_abs = abs(a_n(m_val)) + abs(a_n(m_val + 1)) + abs(a_n(m_val + 2))
assert sum_abs < 13, f"조건(나) 실패: {sum_abs}"

# 검증: 공차가 5
for k in range(1, 20):
    assert a_n(k + 1) - a_n(k) == 5, "공차 오류"

print('VERIFY_PASS')