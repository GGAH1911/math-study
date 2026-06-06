from itertools import product

A = {1, 2, 3, 4}
B = {1, 2, 3}

count_total = 0
count_condition = 0

for f_values in product(B, repeat=4):
    f = {i+1: f_values[i] for i in range(4)}
    count_total += 1
    
    cond1 = f[1] >= 2
    cond2 = set(f.values()) == B
    
    if cond1 or cond2:
        count_condition += 1

prob = count_condition / count_total
expected = 22/27

if abs(prob - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {prob}, expected {expected}')