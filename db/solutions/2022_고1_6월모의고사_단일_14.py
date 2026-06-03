import sympy as sp
k_vals = list(range(5, 20))
count = 0
for k_val in k_vals:
    disc = 4*k_val**2 + 4*k_val - 80
    prod = -k_val + 20
    if disc > 0 and prod > 0:
        count += 1
print('VERIFY_PASS' if count == 15 else 'VERIFY_FAIL')
print(f'Count: {count}')