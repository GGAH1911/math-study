from sympy import symbols, Rational, solve, simplify
x, y = symbols('x y', real=True)
# 대칭이동된 직선: y = (2/3)x + 1
symmetric_line = y - Rational(2, 3) * x - 1
# 점 (9, a)가 이 직선 위에 있는지 검사
a_value = Rational(2, 3) * 9 + 1
if a_value == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')