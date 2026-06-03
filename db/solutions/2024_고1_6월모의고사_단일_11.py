from sympy import symbols, factor

b = 2
a = 10

# 첫 번째 다항식: x^3 + 2x^2 + 3x + 6
P_at_minus_b = (-b)**3 + 2*(-b)**2 + 3*(-b) + 6

# 두 번째 다항식: x^3 + x + a
Q_at_minus_b = (-b)**3 + (-b) + a

if P_at_minus_b == 0 and Q_at_minus_b == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')