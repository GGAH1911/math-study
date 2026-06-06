import sympy as sp

x = sp.Rational(3, 4)

square_area = x**2
triangle_area = (1 - x) * x / 3
total_area = square_area + triangle_area

if total_area == sp.Rational(5, 8):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')