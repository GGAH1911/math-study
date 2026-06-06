from sympy import sqrt, simplify

CANDIDATE = 32

# Step 1: Determine a from the extremum condition at x=1
# For |x|<2: g'(x) = -x + a
# g has extremum at x=1: g'(1) = -1 + a = 0 => a = 1
a = 1
assert -1 + a == 0, "Extremum at x=1 requires a=1"

# Step 2: Verify f(x) values at boundaries
# g'(2) = -2 + 1 = -1, so f(2) = |g'(2)| = 1
# g'(-2) = 2 + 1 = 3, so f(-2) = |g'(-2)| = 3
f_at_2 = abs(-2 + a)
f_at_minus_2 = abs(2 + a)
assert f_at_2 == 1, f"f(2) = {f_at_2}, expected 1"
assert f_at_minus_2 == 3, f"f(-2) = {f_at_minus_2}, expected 3"

# Step 3: Determine b and α
# f is quadratic with double root at x=b (from g'(b)=0 condition)
# f(x) = α(x-b)²
# From constraints: α(2-b)² = 1 and α(2+b)² = 3
# This gives (2+b)²/(2-b)² = 3
# Solving (2+b)/(2-b) = -√3 for |b|>2: b = 4+2√3

b = 4 + 2*sqrt(3)
alpha = (2 - sqrt(3))/8

# Verify quadratic constraints
constraint_1 = simplify(alpha * (2-b)**2)
constraint_2 = simplify(alpha * (2+b)**2)
assert constraint_1 == 1, f"α(2-b)² = {constraint_1}, expected 1"
assert constraint_2 == 3, f"α(2+b)² = {constraint_2}, expected 3"
assert float(b) > 2, f"|b| = {float(b)} is not > 2"

# Step 4: Find zeros of g(x)
# In [-2,2]: g(x) = -x²/2 + x = x(2-x)/2
# Zeros: x=0, x=2

# For x≤-2: g'(x) = f(x) ≥ 0, so g is increasing
# g(-2) = -(-2)²/2 + (-2) = -4 < 0
# So no zeros for x ≤ -2

g_at_minus_2 = -(-2)**2/2 + (-2)
assert g_at_minus_2 == -4, f"g(-2) = {g_at_minus_2}, expected -4"

# For x≥b: g'(x) = f(x) for x≥b (positive after minimum)
# g(b) = α(2-b)³/3 (from integration)
g_b = simplify(alpha * (2-b)**3 / 3)

# At zero for x≥b: g(b) + α(x-b)³/3 = 0
# (x-b)³ = -3g(b)/α
rhs_cubed = simplify(-3 * g_b / alpha)

# Verify (x-b)³ = 80+48√3
expected_cubed = 80 + 48*sqrt(3)
assert simplify(rhs_cubed - expected_cubed) == 0, f"(x-b)³ = {rhs_cubed}, expected {expected_cubed}"

# Verify (2+2√3)³ = 80+48√3
assert simplify((2 + 2*sqrt(3))**3) == 80 + 48*sqrt(3), "Cube root verification failed"

# Third zero: x = b + (2+2√3) = 6+4√3
third_zero = simplify(b + (2 + 2*sqrt(3)))
assert third_zero == 6 + 4*sqrt(3), f"Third zero = {third_zero}, expected 6+4√3"

# Step 5: Sum of all zeros
sum_of_zeros = simplify(0 + 2 + (6 + 4*sqrt(3)))
expected_sum = 8 + 4*sqrt(3)
assert sum_of_zeros == expected_sum, f"Sum = {sum_of_zeros}, expected {expected_sum}"

# Step 6: Extract p and q from sum = p + q√3, compute p×q
# 8 + 4√3 => p=8, q=4
p = 8
q = 4
answer = p * q

# Final verification
if answer == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")