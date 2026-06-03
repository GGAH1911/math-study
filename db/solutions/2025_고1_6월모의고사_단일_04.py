from sympy import symbols, I, re, im, solve

a, b = symbols('a b', real=True)

lhs = a + 4 + b*I
rhs = b + (2-I)*I
rhs_expanded = b + 2*I - I**2
rhs_simplified = b + 1 + 2*I

eq = lhs - rhs_simplified

real_part = re(eq)
imag_part = im(eq)

sol = solve([real_part, imag_part], [a, b])
a_val = sol[a]
b_val = sol[b]

result = a_val + b_val

lhs_check = a_val + 4 + b_val*I
rhs_check = b_val + (2-I)*I
rhs_check_simplified = b_val + 1 + 2*I

if lhs_check == rhs_check_simplified and result == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')