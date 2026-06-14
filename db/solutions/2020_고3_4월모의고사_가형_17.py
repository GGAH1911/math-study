from sympy import symbols, solve, simplify
a, r = symbols('a r', positive=True, real=True)
eq1 = a * (1+r) * (1+r**2) - 45
eq2 = a * (r+1) * (r**4 + r**2 + 1) - 189
sol = solve([eq1, eq2], [a, r])
for s in sol:
    if s[1] > 0:
        a_val, r_val = s
        a3 = a_val * r_val**2
        check1 = sum([a_val * r_val**(k-1) for k in range(1, 5)])
        check2 = sum([(a_val * r_val) * (a_val * r_val**4) / (a_val * r_val**(k-1)) for k in range(1, 7)])
        if abs(check1 - 45) < 1e-9 and abs(check2 - 189) < 1e-9:
            print('VERIFY_PASS')