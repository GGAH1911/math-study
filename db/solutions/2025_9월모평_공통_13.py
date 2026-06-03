from sympy import *
x = symbols('x')
sqrt7 = sqrt(7)
f_neg = -x**2 - 2*x + 6
f_pos = -x**2 + 2*x + 6
P_x = -1 - sqrt7
Q_x = 1 + sqrt7
k_val = 6
A = integrate(f_neg, (x, P_x, 0)) + integrate(f_pos, (x, 0, Q_x))
B = integrate(-f_pos, (x, Q_x, k_val))
diff = simplify(A - 2*B)
print('VERIFY_PASS' if diff == 0 else f'VERIFY_FAIL diff={diff}')