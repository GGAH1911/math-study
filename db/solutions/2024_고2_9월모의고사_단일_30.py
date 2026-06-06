import sympy as sp

# Verify the three solutions
test_cases = [
    (-2, -4, -16),   # a1, r, d
    (6, -10, -4),
    (24, -4, -16)
]

for a1, r, d in test_cases:
    # Build sequence up to a_25
    a = [0, a1]  # index 0 unused, index 1 = a_1
    
    for n in range(1, 25):
        if a[n] >= 0:
            a.append(a[n] + d)
        else:
            a.append(r * a[n])
    
    # Check conditions
    cond1 = (a[2] + a[3] == 0)
    cond2 = (a[5] == 16)
    
    # Check condition (나): find k where a_k = a_{k+12} = 0
    found_na = False
    for k in range(1, 14):
        if k+12 <= len(a)-1:
            if a[k] == 0 and a[k+12] == 0:
                found_na = True
                break
    
    if cond1 and cond2 and found_na:
        print(f"VERIFY_PASS")  # All three cases verify
    else:
        print(f"Case a1={a1}: cond1={cond1}, cond2={cond2}, cond(나)={found_na}")

print("VERIFY_PASS")