from sympy import symbols, solve, simplify

a1, r = symbols('a1 r', positive=True, real=True)

eq1 = a1 * r - 3
eq2 = a1 * r**2 - 6

sols = solve([eq1, eq2], [a1, r])
for sol in sols:
    a1_val, r_val = sol
    a2_val = a1_val * r_val
    a3_val = a1_val * r_val**2
    
    if abs(float(a2_val) - 3) < 1e-9 and abs(float(a3_val) - 6) < 1e-9:
        answer = simplify(a2_val / a1_val)
        if float(answer) == 2.0:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')