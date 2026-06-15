from sympy import symbols, solve

a1, d = symbols('a1 d')

# 조건: S_9 = 27, S_3 = -27 (|S_3| = 27 조건에서)
S_3 = 3*a1 + 3*d
S_9 = 9*a1 + 36*d

eq1 = S_9 - 27
eq2 = S_3 + 27

sol = solve([eq1, eq2], [a1, d])
a1_val = sol[a1]
d_val = sol[d]

# 조건 검증
S_3_check = 3*a1_val + 3*d_val
S_9_check = 9*a1_val + 36*d_val
a_10 = a1_val + 9*d_val

if (S_9_check == 27 and abs(S_3_check) == 27 and 
    d_val > 0 and a_10 == 23):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')