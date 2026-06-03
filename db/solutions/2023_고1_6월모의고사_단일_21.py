from sympy import *
k = Rational(1,16)
# 원래 조건: CD + AB = 4
AB = 2*sqrt(k)
CD = 2*sqrt(3+k)
cond1 = Eq(CD + AB, 4)
print('CD+AB=4 check:', simplify(CD + AB - 4) == 0)
# B 좌표
xB = sqrt(k)
# C 좌표: x^2 - 6x + 6 = k 의 작은 근
x = symbols('x')
roots_cd = solve(x**2 - 6*x + 6 - k, x)
xC = min(roots_cd)
# BC 거리
BC = xC - xB
result = k + BC
print('k + BC =', result)
if result == Rational(17,16):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
