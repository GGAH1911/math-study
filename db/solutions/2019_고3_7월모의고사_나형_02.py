from sympy import symbols, Eq, solve
a, b = symbols('a b', real=True)
# A intersect B = {4}: the only flexible elements are a+2 in A and b in B
a_val = solve(Eq(a+2, 4), a)[0]
b_val = solve(Eq(b, 4), b)[0]
A = {3, a_val+2, 5}
B = {b_val, 6, 8}
if A & B == {4}:
    print(a_val + b_val if (a_val + b_val) == 6 else 'VERIFY_FAIL')
    print('VERIFY_PASS' if (a_val + b_val) == 6 else 'VERIFY_FAIL')
else:
    print('VERIFY_FAIL')