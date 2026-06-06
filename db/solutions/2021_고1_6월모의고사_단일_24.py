from sympy import symbols

CANDIDATE = 22

# Problem: Find minimum a such that x^2 + 8x + (a-6) < 0 has no solution
# For quadratic f(x) = x^2 + 8x + (a-6) with leading coefficient > 0:
# - The inequality f(x) < 0 has solution iff discriminant D > 0
# - The inequality f(x) < 0 has NO solution iff D <= 0

# Discriminant: D = b^2 - 4ac
# b = 8, a_coeff = 1, c = (a-6)
# D = 64 - 4*1*(a-6) = 64 - 4a + 24 = 88 - 4a

# For the inequality to have no solution: D <= 0
# 88 - 4a <= 0
# a >= 22
# Therefore, minimum a = 22

a = symbols('a')
D = 88 - 4*a

# Verification by checking boundary conditions
D_at_min = D.subs(a, CANDIDATE)         # Should be 0 at a=22
D_below_min = D.subs(a, CANDIDATE - 1)  # Should be > 0 at a=21 (has solutions)
D_above_min = D.subs(a, CANDIDATE + 1)  # Should be < 0 at a=23 (no solutions)

# The answer is correct if:
# 1. At a = CANDIDATE, D = 0 (boundary case: parabola touches x-axis)
# 2. At a < CANDIDATE, D > 0 (inequality has solutions)
# 3. At a > CANDIDATE, D < 0 (inequality has no solutions)

if D_at_min == 0 and D_below_min > 0 and D_above_min < 0:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")