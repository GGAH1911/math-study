from sympy import symbols, Eq, solve

k = symbols('k')
eq = Eq(k/1 + 1, 7)
result = solve(eq, k)
k_value = result[0]

f_at_4 = k_value/(4-3) + 1
if f_at_4 == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')