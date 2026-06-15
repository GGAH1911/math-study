from sympy import symbols, Eq, solve
a, b = symbols('a b', real=True)
sol = solve([Eq(a+2, 3), Eq(b-1, 6)], [a, b])
a_val = sol[a]
b_val = sol[b]
A = {a_val + 2, 6}
B = {3, b_val - 1}
result = a_val + b_val
if A == B and result == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')