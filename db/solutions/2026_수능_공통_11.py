from sympy import symbols, integrate, Abs
t = symbols('t')
k = 5
v = t**2 - k*t + 4
integral_0_1 = integrate(v, (t, 0, 1))
integral_1_2 = integrate(v, (t, 1, 2))
distance = Abs(integral_0_1) + Abs(integral_1_2)
if distance == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')