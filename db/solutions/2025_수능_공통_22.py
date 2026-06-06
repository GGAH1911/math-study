import sympy as sp

def verify_sequence(a1):
    seq = [a1]
    for _ in range(4):
        an = seq[-1]
        if an == 0 or abs(an) % 2 == 0:
            an_next = an // 2
        else:
            an_next = an - 3
        seq.append(an_next)
    return seq

candidates = [6, 7, 8, 10, -9, -24]
all_valid = True

for a1 in candidates:
    seq = verify_sequence(a1)
    a1_val, a2_val, a3_val, a4_val, a5_val = seq[:5]
    
    cond1 = (abs(a1_val) != abs(a3_val))
    cond2 = (abs(a2_val) != abs(a4_val))
    cond3 = (abs(a3_val) == abs(a5_val))
    
    if not (cond1 and cond2 and cond3):
        all_valid = False

if all_valid:
    total = sum(abs(a1) for a1 in candidates)
    print('VERIFY_PASS' if total == 64 else 'VERIFY_FAIL')
else:
    print('VERIFY_FAIL')