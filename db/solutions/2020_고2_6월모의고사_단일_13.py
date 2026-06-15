from sympy import symbols, log, Eq, solve, Rational, simplify

k = symbols('k', positive=True)

# Given: M_A=4.8, L_A=L; M_B=1.3, L_B=k*L
# Formula: M_A - M_B = -2.5 * log(L_A / L_B, 10)
# => 4.8 - 1.3 = -2.5 * log(1/k, 10) = 2.5 * log(k, 10)

lhs = Rational(48, 10) - Rational(13, 10)  # 3.5
equation = Eq(lhs, Rational(5, 2) * log(k, 10))

solution = solve(equation, k)
CANDIDATE = solution[0]

# Verify candidate satisfies original equation
lhs_check = Rational(48, 10) - Rational(13, 10)
rhs_check = -Rational(5, 2) * log(1 / CANDIDATE, 10)

diff = simplify(lhs_check - rhs_check)
if diff == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
