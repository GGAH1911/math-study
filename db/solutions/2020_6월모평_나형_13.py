from sympy import symbols, solve, simplify
n = symbols('n', integer=True, positive=True)
alpha = (n+1)/3
beta = (2*n-1)/3
eq1 = alpha + beta - n
eq2 = alpha*beta - 4*(n-4)
sol_n = solve(eq2, n)
for val in sol_n:
    if val.is_integer and val > 0:
        a_val = float((val+1)/3)
        b_val = float((2*val-1)/3)
        if abs(a_val + b_val - val) < 1e-9 and abs(a_val*b_val - 4*(val-4)) < 1e-9:
            if a_val < b_val and abs((b_val - a_val) - (a_val - 1)) < 1e-9:
                print('VERIFY_PASS')