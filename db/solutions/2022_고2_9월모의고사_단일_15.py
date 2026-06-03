from sympy import symbols, solve, simplify

a, k = symbols('a k', positive=True, integer=True)

eq1 = a + 2*k - 33
eq2 = (k+10)*(a + k + 9) - 640

sols = solve([eq1, eq2], [a, k])
print(f'Solutions: {sols}')

for sol in sols:
    a_val, k_val = sol
    if a_val > 0:
        a_n = a_val + 2*(k_val - 1)
        s_k = k_val * (2*a_val + (k_val-1)*2) / 2
        s_k_plus_10 = (k_val+10) * (2*a_val + (k_val+10-1)*2) / 2
        
        check1 = (a_val + 2*k_val - 2 == 31)
        check2 = (s_k_plus_10 == 640)
        
        if check1 and check2:
            print(f'VERIFY_PASS' if s_k == 220 else f'Result: {s_k}')
        else:
            print(f'VERIFY_FAIL')