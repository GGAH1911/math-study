from sympy import symbols, expand, simplify

x, a = symbols('x a')
lhs = (x - 1)**2 + a*x
rhs = x**2 + 1

# 등식이 모든 x에 대해 성립하려면
eq = expand(lhs - rhs)
print(f'LHS - RHS = {eq}')

# (a-2)x = 0이 모든 x에 대해 성립하려면 a = 2
a_val = 2
eq_check = eq.subs(a, a_val)
print(f'a=2 일 때: {eq_check}')

if eq_check == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')