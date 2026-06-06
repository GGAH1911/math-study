from sympy import symbols, solve, Rational, simplify
x = symbols('x')
m_opt = Rational(1, 3)
f = Rational(1, 2) * x**2 - 2*x
B_x = 4 + 2*m_opt
B_y = 4*m_opt + 2*m_opt**2
C_x = 2*m_opt
C_y = 2*m_opt**2 - 4*m_opt
S1 = abs((4 - C_x) * C_y) / 2
S2 = abs((B_x - 4) * B_y) / 2
diff = S1 - S2
if diff == Rational(4, 3):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')