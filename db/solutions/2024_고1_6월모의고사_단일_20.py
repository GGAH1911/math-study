import sympy as sp
x, a = sp.symbols('x a', real=True)

# a = 2 검증
a_val = 2
f = x**3 - (a_val**2 + a_val - 1)*x**2 - a_val*(a_val - 3)*x + 4*a_val
roots_a2 = sp.solve(f, x)
roots_a2_sorted = sorted([float(r) for r in roots_a2])
alpha_a2, beta_a2, gamma_a2 = roots_a2_sorted
check_a2 = (alpha_a2 * gamma_a2 == -4 and alpha_a2 < beta_a2 < gamma_a2)

# a = -1 검증
a_val = -1
f = x**3 - (a_val**2 + a_val - 1)*x**2 - a_val*(a_val - 3)*x + 4*a_val
roots_a_minus1 = sp.solve(f, x)
roots_a_minus1_sorted = sorted([float(r) for r in roots_a_minus1])
alpha_a_minus1, beta_a_minus1, gamma_a_minus1 = roots_a_minus1_sorted
check_a_minus1 = (alpha_a_minus1 * gamma_a_minus1 == -4 and alpha_a_minus1 < beta_a_minus1 < gamma_a_minus1)

# a = -2 검증
a_val = -2
f = x**3 - (a_val**2 + a_val - 1)*x**2 - a_val*(a_val - 3)*x + 4*a_val
roots_a_minus2 = sp.solve(f, x)
roots_a_minus2_sorted = sorted([float(r) for r in roots_a_minus2])
alpha_a_minus2, beta_a_minus2, gamma_a_minus2 = roots_a_minus2_sorted
check_a_minus2 = (alpha_a_minus2 * gamma_a_minus2 == -4 and alpha_a_minus2 < beta_a_minus2 < gamma_a_minus2)

if check_a2 and check_a_minus1 and not check_a_minus2 and (2 + (-1) == 1):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')