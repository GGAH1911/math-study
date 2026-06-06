from sympy import symbols, solve, simplify

alpha, beta, k = symbols('alpha beta k', complex=True)

# k = 6
k_val = 6

# alpha, beta are roots of x^2 - 3x + k = 0
# So alpha + beta = 3, alpha*beta = k = 6
# Solve for alpha, beta
roots = solve(symbols('x')**2 - 3*symbols('x') + k_val, symbols('x'))
alpha_val, beta_val = roots[0], roots[1]

# Verify the condition
lhs = 1/(alpha_val**2 - alpha_val + k_val) + 1/(beta_val**2 - beta_val + k_val)
lhs_simplified = simplify(lhs)

if abs(lhs_simplified - 1/4) < 1e-10:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {lhs_simplified} != 0.25')