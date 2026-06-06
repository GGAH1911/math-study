import sympy as sp

def a(n):
    return sp.Rational(1, n**2)

# 조건 검증: a_1 = 1
assert a(1) == 1

# 조건 검증: 텔레스코핑 합
for n in range(2, 11):
    tele_sum = sum(sp.sqrt(a(k)) - sp.sqrt(a(k+1)) for k in range(1, n))
    expected = sp.Rational(n-1, n)
    assert sp.simplify(tele_sum - expected) == 0

# 최종 답
answer = sum(1/a(k) for k in range(1, 11))
assert answer == 385
print('VERIFY_PASS')