from sympy import symbols, solve, N
import math

CANDIDATE = 729

# Define f(x) = (x+2)^4 - 16(x+2)^2 + 4
def f(x_val):
    u = x_val + 2
    return u**4 - 16*u**2 + 4

def f_prime(x_val):
    u = x_val + 2
    return 4*u**3 - 32*u

# Verify f(2) = 4 (given condition)
assert f(2) == 4, "Condition f(2) = 4 failed"

# Verify f'(2) > 0 (given condition)
assert f_prime(2) > 0, f"Condition f'(2) > 0 failed: f'(2) = {f_prime(2)}"

# Calculate f(4)
f_4_value = f(4)
# (4+2)^4 - 16*(4+2)^2 + 4 = 6^4 - 16*36 + 4 = 1296 - 576 + 4 = 724
assert f_4_value == 724, f"f(4) should be 724, got {f_4_value}"

# Find critical points of f: f'(x) = 0
# 4(x+2)^3 - 32(x+2) = 0
# 4(x+2)[(x+2)^2 - 8] = 0
# Solutions: x = -2, -2-2√2, -2+2√2
x = symbols('x')
critical_points = solve(4*(x+2)**3 - 32*(x+2), x)
assert len(critical_points) == 3, f"Should have 3 critical points, got {len(critical_points)}"

# Find roots where f(x) = 4
# (x+2)^4 - 16(x+2)^2 + 4 = 4
# (x+2)^4 - 16(x+2)^2 = 0
# (x+2)^2[(x+2)^2 - 16] = 0
# (x+2)^2 = 0 or (x+2)^2 = 16
# Solutions: x = -2, 2, -6
roots_at_4 = solve((x+2)**4 - 16*(x+2)**2, x)

# Verify all critical points satisfy f'(x) = 0
for cp in critical_points:
    assert abs(f_prime(cp)) < 1e-10, f"Critical point {cp} doesn't satisfy f'(x) = 0"

# Verify all roots satisfy f(x) = 4
for root in roots_at_4:
    assert abs(f(root) - 4) < 1e-10, f"Root {root} doesn't satisfy f(x) = 4"

# h(t) = |C ∪ S_t| where C = critical points, S_t = {x : f(x) = t}
# For t = 4: C = {-2, -2-2√2, -2+2√2}, S_4 = {-2, 2, -6}
# C ∪ S_4 = {-2, -2-2√2, -2+2√2, 2, -6} has 5 distinct elements

critical_floats = sorted([float(N(cp)) for cp in critical_points])
roots_floats = sorted([float(N(r)) for r in roots_at_4])

# Merge with tolerance for floating-point comparison
merged = []
for val in critical_floats + roots_floats:
    is_duplicate = any(abs(val - m) < 1e-10 for m in merged)
    if not is_duplicate:
        merged.append(val)

h_4_value = len(merged)
assert h_4_value == 5, f"h(4) should be 5, got {h_4_value}"

# Final calculation: f(4) + h(4)
result = f_4_value + h_4_value

if result == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")