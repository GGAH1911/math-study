from sympy import symbols, cos, pi, simplify

# 주어진 조건
AB = 6
AC = 8
cos_A = -1/4

# 코사인 법칙: BC² = AB² + AC² - 2·AB·AC·cos(A)
BC_squared = AB**2 + AC**2 - 2*AB*AC*cos_A

# 검증
result = int(BC_squared)
if result == 124:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')