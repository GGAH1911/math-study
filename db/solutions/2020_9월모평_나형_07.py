from sympy import symbols, solve, Eq

a1, d = symbols('a1 d')
eq1 = Eq(a1, a1 + 2*d + 8)
eq2 = Eq(2*(a1 + 3*d) - 3*(a1 + 5*d), 3)

sol = solve([eq1, eq2], [a1, d])
a1_val, d_val = sol[a1], sol[d]

for k in range(1, 20):
    a_k = a1_val + (k-1)*d_val
    if a_k < 0:
        if k == 10 and a_k == -3:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')
        break