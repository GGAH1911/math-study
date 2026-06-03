from sympy import symbols, Rational, simplify
C_B, V_B = symbols('C_B V_B', positive=True, real=True)
C_A = 3 * C_B
V_A = Rational(2, 3) * V_B
U_A = Rational(1, 2) * C_A * V_A**2
U_B = Rational(1, 2) * C_B * V_B**2
ratio = simplify(U_A / U_B)
if ratio == Rational(4, 3):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')