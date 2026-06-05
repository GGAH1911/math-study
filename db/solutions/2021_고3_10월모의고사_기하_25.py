from sympy import symbols, Rational, discriminant, Poly, expand

a_val = 10
c_val = Rational(5, 1)

x, y = symbols('x y')

# 타원 접선 검증: y = x/2 + 5 대입
y_line = x * Rational(1,2) + c_val
ellipse_expr = x**2/36 + y_line**2/16 - 1
ellipse_poly = Poly(expand(ellipse_expr * 144), x)
disc_e = discriminant(ellipse_poly, x)

# 포물선 접선 검증: y^2 - 2ay + 2ac = 0
para_poly = Poly(y**2 - 2*a_val*y + 2*a_val*c_val, y)
disc_p = discriminant(para_poly, y)

focus_x = Rational(a_val, 4)

if disc_e == 0 and disc_p == 0 and focus_x == Rational(5, 2):
    print('VERIFY_PASS')
else:
    print(f'disc_e={disc_e}, disc_p={disc_p}, focus_x={focus_x}')
    print('VERIFY_FAIL')
