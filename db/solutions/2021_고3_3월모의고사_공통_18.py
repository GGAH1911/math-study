from sympy import symbols, integrate, Abs, simplify

k = 9
x = symbols('x')

# F(x) for x < 0
F_neg = -x**2

# F(x) for x >= 0
F_pos = k * (x**2 - x**3/3)

# Calculate F(2) and F(-3)
F_2 = F_pos.subs(x, 2)
F_minus3 = F_neg.subs(x, -3)

# Check the condition
difference = F_2 - F_minus3

if difference == 21:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')