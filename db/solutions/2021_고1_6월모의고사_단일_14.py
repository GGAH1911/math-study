from sympy import symbols, Eq, solve
m_B, v_B, r_B = symbols('m_B v_B r_B', positive=True, real=True)
m_A = 3 * m_B
v_A = v_B / 2
r_A = 3 * r_B / 4
F_A = m_A * (v_A ** 2) / r_A
F_B = m_B * (v_B ** 2) / r_B
if abs(float(F_A.subs([(m_B, 1), (v_B, 1), (r_B, 1)]) - F_B.subs([(m_B, 1), (v_B, 1), (r_B, 1)]))) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')