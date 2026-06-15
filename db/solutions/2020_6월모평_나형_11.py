from sympy import symbols, limit, oo, Rational

n = symbols('n', integer=True, positive=True)
r = Rational(3, 2)

# 조건 1: 급수 수렴 확인 (일반항이 0으로 수렴)
general_term = 2*r - 3
assert general_term == 0, f"일반항 수렴 조건 실패: {general_term}"

# 조건 2: 극한값 계산
expression = (r**(n+2) - 1) / (r**n + 1)
result = limit(expression, n, oo)

expected = Rational(9, 4)
assert result == expected, f"극한값 불일치: {result} != {expected}"

print('VERIFY_PASS')