import sympy as sp
z = sp.Symbol('z')
m_val = -8
n_val = 17
eq = z**2 + m_val*z + n_val
roots = sp.solve(eq, z)
z_test = roots[0]
z_bar = sp.conjugate(z_test)
check1 = sp.simplify(z_test**2 + m_val*z_test + n_val)
check2 = z_test + z_bar
if check1 == 0 and check2 == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')