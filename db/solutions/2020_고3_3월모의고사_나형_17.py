from sympy import symbols, Eq, solve

k_var = symbols('k', integer=True, positive=True)
d = 54 / (5 - k_var)
a1 = 42 - 2*d

eq2 = Eq(a1 + (k_var - 1)*d/2, k_var)
sol = solve(eq2, k_var)

for k_val in sol:
    if k_val >= 4 and k_val == int(k_val):
        k_val = int(k_val)
        d_val = 54 / (5 - k_val)
        a1_val = 42 - 2*d_val
        S_k = k_val*a1_val + k_val*(k_val-1)*d_val/2
        a_k_minus_3 = a1_val + (k_val-4)*d_val
        a_k_minus_1 = a1_val + (k_val-2)*d_val
        
        if abs(S_k - k_val**2) < 1e-9 and abs(a_k_minus_3 + a_k_minus_1 - (-24)) < 1e-9:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')