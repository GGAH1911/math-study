from sympy import symbols, diff, solve, simplify, Rational

t = symbols('t', positive=True, real=True)
f = 2*t**3 - 7*t**2 + 1
f_prime = diff(f, t)

# Point (t, f(t))
f_t = f.subs(t, t)
f_prime_t = f_prime.subs(t, t)

# Tangent line at (t, f(t)): y - f(t) = f'(t)(x - t)
# Passes through (0, 1): 1 - f(t) = f'(t)(0 - t)
condition = 1 - f_t - f_prime_t * (0 - t)
condition = simplify(condition)

# Solve for t
solutions = solve(condition, t)
print(f"Solutions: {solutions}")

# Filter positive solutions
positive_sols = [sol for sol in solutions if sol > 0]
print(f"Positive solution: {positive_sols}")

if positive_sols:
    t_val = positive_sols[0]
    # Verify: Check tangent line passes through (0, 1)
    f_at_t = f.subs(t, t_val)
    slope_at_t = f_prime.subs(t, t_val)
    # y - f(t) = slope(x - t), at x=0: y = f(t) + slope*(0-t) = f(t) - slope*t
    y_at_0 = f_at_t - slope_at_t * t_val
    y_at_0_simplified = simplify(y_at_0)
    print(f"t = {t_val}")
    print(f"f(t) = {simplify(f_at_t)}")
    print(f"f'(t) = {simplify(slope_at_t)}")
    print(f"Tangent line at x=0 gives y = {y_at_0_simplified}")
    
    if y_at_0_simplified == 1:
        print("VERIFY_PASS")
    else:
        print("VERIFY_FAIL")
else:
    print("VERIFY_FAIL")