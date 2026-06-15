from sympy import Rational, nsimplify

# 원래 조건: 공 60개 (1->10, 2->20, 3->30), 복원추출 10회 합 = Y
counts = {1: 10, 2: 20, 3: 30}
total = sum(counts.values())  # 60
P = {x: Rational(c, total) for x, c in counts.items()}

# 확률 합 = 1 검증
assert sum(P.values()) == 1

# E(X), E(X^2), V(X)
EX = sum(x * P[x] for x in P)
EX2 = sum(x**2 * P[x] for x in P)
VX = EX2 - EX**2

# 문제 명시값 E(X)=7/3 확인
assert EX == Rational(7, 3)

n = 10
# (가) p = V(X)
p = VX
# (나) q = V(Xbar) = V(X)/n
q = VX / n
# E(Xbar)=7/3 확인
assert EX == Rational(7, 3)
# (다) r = V(Y), Y = 10 * Xbar = sum of 10 i.i.d. X  -> V(Y)=n*V(X)=100*V(Xbar)
r = n**2 * (VX / n)
assert r == n * VX  # 두 방식 일치
# E(Y)=70/3 확인
assert n * EX == Rational(70, 3)

ans = p + q + r

# 보기 값들
options = {1: Rational(31,6), 2: Rational(11,2), 3: Rational(35,6),
           4: Rational(37,6), 5: Rational(13,2)}

if p == Rational(5,9) and q == Rational(1,18) and r == Rational(50,9) and ans == Rational(37,6) and options[4] == ans:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
