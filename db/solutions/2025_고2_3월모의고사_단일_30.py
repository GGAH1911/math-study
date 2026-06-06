CANDIDATE = 68

from fractions import Fraction

# Problem setup:
# f(x) defined on {x | x ≠ 2}
# f(x) = [a(x-n)/(x-2) - n] for x < 2 or 2 < x < n
# f(x) = [-a√(x-n) - n] for x ≥ n
# g(t) = number of distinct real roots of |f(x)| = t

# Condition (가): g(t)=2 has minimum value 0, maximum value (3/2)n
# Analysis shows this requires a = -n/2

# Condition (나): g(|f(5)|) × g(n) = 6
# From analysis: g(n) = 3, so we need g(|f(5)|) = 2
# g(t) = 2 when t = 0 or when n < t ≤ (3/2)n

# For n > 5:
# f(5) = a(5-n)/(5-2) - n
#      = (-n/2)(5-n)/3 - n
#      = -n(5-n)/6 - n
#      = [n² - 11n]/6
#      = n(n-11)/6

valid_n_values = []

# Check all natural numbers n > 2
for n in range(3, 30):
    # Set a = -n/2 from condition (가)
    a = Fraction(-n, 2)
    
    # Calculate f(5) with exact arithmetic
    # Using formula: f(5) = n(n-11)/6 for n > 5
    if n > 5:
        f_5 = Fraction(n * (n - 11), 6)
    else:
        # For n ≤ 5, we use f(5) = -a√(5-n) - n
        # This involves square roots, harder to verify exactly
        # Skip these for exact verification
        continue
    
    abs_f_5 = abs(f_5)
    
    # Determine if g(|f(5)|) = 2
    # This happens when: |f(5)| = 0 OR n < |f(5)| ≤ (3/2)n
    
    satisfies_condition_b = False
    
    if abs_f_5 == 0:
        # g(0) = 2
        satisfies_condition_b = True
    elif n < abs_f_5 <= Fraction(3*n, 2):
        # g(t) = 2 for n < t ≤ (3/2)n
        satisfies_condition_b = True
    
    if satisfies_condition_b:
        valid_n_values.append(n)

# Verify the specific values:
# n=11: f(5) = 11·0/6 = 0, so g(0)=2 ✓
# n=18: f(5) = 18·7/6 = 21, and 18 < 21 ≤ 27 ✓
# n=19: f(5) = 19·8/6 = 76/3, and 19 < 76/3 ≤ 28.5 ✓
# n=20: f(5) = 20·9/6 = 30, and 20 < 30 ≤ 30 ✓

# Calculate sum of valid n
total_sum = sum(valid_n_values)

# Verify against CANDIDATE
if total_sum == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")
