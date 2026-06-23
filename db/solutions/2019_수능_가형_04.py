from sympy import Rational, symbols, Eq, solve
# 미지의 분할 확률: a=P(A&B), b=P(A&B^C), c=P(A^C&B), d=P(A^C&B^C)
a,b,c,d = symbols('a b c d', nonnegative=True)
PA = Rational(1,3)
PAcB = Rational(1,6)  # P(A^C & B)
eqs = [
    Eq(a+b, PA),        # P(A) = P(A&B)+P(A&B^C)
    Eq(c, PAcB),        # P(A^C & B)
    Eq(b, 0),           # A, B^C 배반 => P(A & B^C)=0
    Eq(a+b+c+d, 1)      # 전체 확률 합 = 1
]
sol = solve(eqs, [a,b,c,d], dict=True)[0]
PB = sol[a] + sol[c]   # P(B) = P(A&B)+P(A^C&B)
# 조건 만족 검증: 모든 확률 >=0, 배반조건, 주어진 값
ok = (sol[b]==0) and (sol[a]+sol[b]==PA) and (sol[c]==PAcB) and all(v>=0 for v in sol.values())
print('VERIFY_PASS' if (ok and PB==Rational(1,2)) else 'VERIFY_FAIL')
