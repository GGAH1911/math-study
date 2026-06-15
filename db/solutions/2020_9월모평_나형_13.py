from sympy import symbols, Eq, solve, Rational
m = symbols('m', positive=True)
# X ~ N(m, (m/3)^2)
# P(X <= 9/2) = 0.9987 => z-score = 3 (since P(0<=Z<=3) = 0.4987, P(Z<=3)=0.9987)
# (9/2 - m) / (m/3) = 3
z_val = Rational(9, 2)
eq = Eq((z_val - m) / (m / 3), 3)
sol = solve(eq, m)
m_val = sol[0]
print('m =', m_val)
# Verify: z-score should be exactly 3
z_check = (Rational(9,2) - m_val) / (m_val / 3)
print('z-score =', z_check)
if m_val == Rational(9, 4) and z_check == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
