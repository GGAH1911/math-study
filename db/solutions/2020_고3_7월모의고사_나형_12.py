from sympy import symbols, Eq, solve
a, b = symbols('a b', real=True, positive=True)
eq1 = Eq(4*a + b, 80)
eq2 = Eq(10*a / (10*a + b), 5/8)
sol = solve([eq1, eq2], [a, b])
if sol:
    a_val, b_val = sol[a], sol[b]
    total = 10*a_val + b_val + (48 - 2*a_val) + (b_val - 8)
    cond_prob = 10*a_val / (10*a_val + b_val)
    if abs(total - 200) < 1e-9 and abs(cond_prob - 5/8) < 1e-9:
        answer = b_val - a_val
        if abs(answer - 40) < 1e-9:
            print('VERIFY_PASS')
        else:
            print(f'VERIFY_FAIL: calculated {answer}')
    else:
        print('VERIFY_FAIL: conditions not met')
else:
    print('VERIFY_FAIL: no solution')