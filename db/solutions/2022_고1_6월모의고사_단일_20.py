import sympy as sp
x, a = sp.symbols('x a', real=True)

# a=4 cases
a_val = 4
P1 = x - 8
P2 = -x + 4

for P in [P1, P2]:
    lhs = (P + 2)**2
    rhs = (x - a_val) * (x - 2*a_val) + 4
    if sp.simplify(lhs - rhs) == 0:
        print(f'a=4, P(x)={P}: VERIFIED')

# a=-4 cases
a_val = -4
P3 = x + 4
P4 = -x - 8

for P in [P3, P4]:
    lhs = (P + 2)**2
    rhs = (x - a_val) * (x - 2*a_val) + 4
    if sp.simplify(lhs - rhs) == 0:
        print(f'a=-4, P(x)={P}: VERIFIED')

# Sum of P(1) values
P_values = [P.subs(x, 1) for P in [P1, P2, P3, P4]]
sum_P1 = sum(P_values)
if sum_P1 == -8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')