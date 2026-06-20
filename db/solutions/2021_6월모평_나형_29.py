from itertools import product

CANDIDATE = 15

A = [1, 2, 3, 4]
count = 0
total = 0

for f_vals in product(A, repeat=4):
    total += 1
    
    # 조건 (가): f(1) × f(2) ≥ 9
    if f_vals[0] * f_vals[1] < 9:
        continue
    
    # 조건 (나): 함수 f의 치역의 원소 개수는 3
    if len(set(f_vals)) != 3:
        continue
    
    count += 1

p = count / total
computed_answer = int(120 * p)

if computed_answer == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')