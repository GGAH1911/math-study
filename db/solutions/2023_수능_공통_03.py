import sympy as sp

a1 = 48
r = sp.Rational(1, 2)

# 등비수열 항들
a2 = a1 * r
a4 = a1 * r**3
a6 = a1 * r**5

# 조건 검증
cond1 = a2 + a4
cond2 = a4 + a6

if cond1 == 30 and cond2 == sp.Rational(15, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')