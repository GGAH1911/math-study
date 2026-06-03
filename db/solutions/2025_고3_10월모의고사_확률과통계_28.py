import sympy as sp
from sympy import sqrt, erf, Rational

# 원 문제 그대로: X ~ N(m, (1/(2m))^2), a<0, m!=0
# 조건1: P(X<=a)+P(X<=a^2)=1
# 조건2: P(X<=a^2+a)=0.9772  (표준정규표값)
# 답: P(X<=-a/8)

m = Rational(1)
sigma = Rational(1, 2) / m  # 1/(2m)
a = Rational(-2)

def Phi_X(x):
    z = (x - m) / sigma
    return (1 + erf(z / sqrt(2))) / 2

c1 = Phi_X(a) + Phi_X(a**2)
c2 = Phi_X(a**2 + a)
ans = Phi_X(-a / 8)

c1f = float(c1)
c2f = float(c2)
ansf = float(ans)

# 표값 기반 비교: P(Z<=2.0)=0.5+0.4772=0.9772, P(Z<=-1.5)=0.5-0.4332=0.0668
ok1 = abs(c1f - 1.0) < 1e-6
ok2 = abs(c2f - 0.9772) < 5e-4
ok3 = abs(ansf - 0.0668) < 5e-4

print('VERIFY_PASS' if (ok1 and ok2 and ok3) else 'VERIFY_FAIL')