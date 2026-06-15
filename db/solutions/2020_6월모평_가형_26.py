from sympy import symbols, solve, sqrt

CANDIDATE = 48

a, b = symbols('a b', real=True, positive=True)

# Condition 1: a^2 + b^2 = 100
eq1 = a**2 + b**2 - 100

# Condition 2: |b - a| = 2 with a > b > 0, so a - b = 2
eq2 = a - b - 2

# Solve the system
solutions = solve([eq1, eq2], [a, b])
valid_solutions = [(sol[0], sol[1]) for sol in solutions if sol[0] > sol[1] > 0]

if valid_solutions:
    a_val, b_val = valid_solutions[0]
    ab_product = a_val * b_val
    
    # Verify the angle condition
    cos_theta = abs(b_val - a_val) / (10 * sqrt(2))
    expected_cos = sqrt(2) / 10
    
    if ab_product == CANDIDATE and cos_theta == expected_cos:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')