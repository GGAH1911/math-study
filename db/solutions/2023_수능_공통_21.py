import math

CANDIDATE = 33

def count_roots_for_t(t, n):
    """
    Count the number of real roots of f(x) = t, where
    f(x) = |3^(x+2) - n| for x < 0
    f(x) = |log_2(x+4) - n| for x >= 0
    """
    root_count = 0
    
    # For x < 0: |3^(x+2) - n| = t
    # This gives 3^(x+2) = n + t or 3^(x+2) = n - t
    # Since x < 0, we have 3^(x+2) < 3^2 = 9
    
    # Case 1: 3^(x+2) = n + t
    # Valid if 0 < n + t < 9
    if 0 < n + t < 9:
        # x = log_3(n + t) - 2 < 0 iff n + t < 9 ✓
        root_count += 1
    
    # Case 2: 3^(x+2) = n - t
    # Valid if 0 < n - t < 9
    if t > 0 and 0 < n - t < 9:
        # x = log_3(n - t) - 2 < 0 iff n - t < 9 ✓
        root_count += 1
    
    # For x >= 0: |log_2(x+4) - n| = t
    # This gives log_2(x+4) = n + t or log_2(x+4) = n - t
    # x >= 0 means x + 4 >= 4, so log_2(x+4) >= 2
    
    # Case 3: log_2(x+4) = n + t
    # This gives x + 4 = 2^(n+t), so x = 2^(n+t) - 4
    # Valid if 2^(n+t) - 4 >= 0, i.e., n + t >= 2
    if n + t >= 2:
        root_count += 1
    
    # Case 4: log_2(x+4) = n - t
    # This gives x + 4 = 2^(n-t), so x = 2^(n-t) - 4
    # Valid if 2^(n-t) - 4 >= 0, i.e., n - t >= 2
    if t > 0 and n - t >= 2:
        root_count += 1
    
    return root_count

def find_g_max(n):
    """Find the maximum value of g(t) = root count of f(x)=t"""
    max_g = 0
    
    # Sample t values in a fine grid to find maximum
    # Check both integer and fractional parts
    for t_val_int in range(0, 20):
        for t_val_frac in range(0, 100):
            t = t_val_int + t_val_frac / 100.0
            g_t = count_roots_for_t(t, n)
            max_g = max(max_g, g_t)
    
    return max_g

# Find all natural numbers n for which g(t) has maximum value 4
valid_n_values = []
for n in range(1, 25):
    g_max_value = find_g_max(n)
    if g_max_value == 4:
        valid_n_values.append(n)

# Calculate the sum of all valid n
answer = sum(valid_n_values)

# Verify against CANDIDATE
if answer == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")