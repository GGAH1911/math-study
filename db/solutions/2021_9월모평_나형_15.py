import sympy as sp
from sympy import symbols, solve, log, simplify

# 정의
x1, x2, a, b = 2, 8, sp.Rational(1,3), sp.Rational(1,3)

# 조건 1: AB = 6√2
AB = sp.sqrt((x2 - x1)**2 + (x2 - x1)**2)
check1 = sp.simplify(AB - 6*sp.sqrt(2))

# 조건 2: 사각형 ACDB 넓이 = 30
area = sp.Rational(1,2) * (x2**2 - x1**2)
check2 = area - 30

# 조건 3: 교점 조건
check3a = 2**(a*x1 + b) - x1
check3b = 2**(a*x2 + b) - x2

if check1 == 0 and check2 == 0 and abs(float(check3a)) < 1e-10 and abs(float(check3b)) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')