from sympy import symbols, summation, Rational
n = symbols('n', integer=True)
# 도형 R의 넓이: 단위정사각형 3개
area_R = 3
# 2n개의 도형을 겹치지 않고 빈틈없이 붙여 만든 직사각형의 넓이
a_n = 2*n*area_R  # = 6n
total = summation(a_n, (n, 10, 15))
expected = 450
if total == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', total)