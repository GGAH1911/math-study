from sympy import symbols, solve, diff

x, a, b = symbols('x a b', real=True)

f_left = x**3 + a*x + b
f_right = b*x + 4

# 연속성: 1 + a + b = b + 4
continuity_eq = (1 + a + b) - (b + 4)

# 미분가능성: (3 + a) = b
f_left_deriv = diff(f_left, x)
f_right_deriv = diff(f_right, x)
f_left_deriv_at_1 = f_left_deriv.subs(x, 1)
differentiability_eq = f_left_deriv_at_1 - f_right_deriv

sol = solve([continuity_eq, differentiability_eq], [a, b])
a_val = sol[a]
b_val = sol[b]
answer = a_val + b_val

if answer == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')