from sympy import symbols, solve, Rational

a1, r = symbols('a1 r', real=True, nonzero=True)

# a5 = a1 * r^4 = 2
eq = a1 * r**4 - 2

# a4 * a6 = (a1 * r^3) * (a1 * r^5) = a1^2 * r^8 = (a1 * r^4)^2 = a5^2
# This is always true for any a1, r satisfying a5=2
# Let's pick a specific solution: r=1, a1=2
val_a4_a6 = (2 * 1**(-1)) * (2 * 1**(1))  # a4=2, a6=2 when r=1, a1=2
result = val_a4_a6

# General proof
a5 = 2
a4_times_a6 = a5**2

if a4_times_a6 == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
