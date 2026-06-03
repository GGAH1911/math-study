from sympy import Rational

a1 = Rational(5, 3)
d = Rational(1, 3)

# 조건 (가): a_5는 자연수
a5 = a1 + 4*d
assert a5 == 3 and a5.is_integer and a5 > 0

# 조건 (나): S_8 = 68/3
S8 = 4*(2*a1 + 7*d)
assert S8 == Rational(68, 3)

# 공차 조건
assert 0 < d < 1

# 답 검증
a16 = a1 + 15*d
assert a16 == Rational(20, 3)

print('VERIFY_PASS')