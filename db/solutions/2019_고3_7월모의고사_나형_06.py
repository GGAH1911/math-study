from sympy import symbols, solve
a = symbols('a')
left_limit = 2 + 1
func_at_2 = 2**2 - 4*2 + a
a_solution = solve(left_limit - func_at_2, a)[0]
if a_solution == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')