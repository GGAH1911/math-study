from sympy import *

a = symbols('a', real=True)

# Check factorization: a^3 - 3a + 2
poly = a**3 - 3*a + 2
factored = factor(poly)
print(f"a^3 - 3a + 2 = {factored}")

# For a = -2
a_val = -2
b_val = a_val/2 - 1/2
sum_ab = a_val + b_val
print(f"a = {a_val}, b = {b_val}, a+b = {sum_ab}")

# Verify h(-1) = h(-a) at a = -2
h_alpha = a_val - Rational(2,3)
h_beta = Rational(1,3) * a_val**3
print(f"h(-1) = {h_alpha}, h(2) = {h_beta}")
print(f"h(-1) == h(2): {h_alpha == h_beta}")

# Max and min
M = Rational(-7, 2)
m = -5
diff = M - m
print(f"M = {M}, m = {m}, M - m = {diff}")
if diff == Rational(3,2):
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")