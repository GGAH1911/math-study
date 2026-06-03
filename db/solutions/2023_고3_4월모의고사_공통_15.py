import math

def next_a(a_n, n):
    if a_n < 1:
        return 2 ** (n - 2)
    else:
        return math.log2(a_n)

def simulate(a1):
    a = a1
    seq = [a1]
    for n in range(1, 6):
        a = next_a(a, n)
        seq.append(a)
    return seq

pass_all = True

# Test a1 in [2, 4) - sample several points
for a1_test in [2.0, 2.5, 3.0, 3.5, 3.999]:
    seq = simulate(a1_test)
    a5, a6 = seq[4], seq[5]
    if abs(a5 + a6 - 1) > 1e-9:
        pass_all = False
        print(f'FAIL: a1={a1_test}, a5+a6={a5+a6}')

# Test a1 = 2^16
a1_test = 2**16
seq = simulate(a1_test)
a5, a6 = seq[4], seq[5]
if abs(a5 + a6 - 1) > 1e-9:
    pass_all = False
    print(f'FAIL: a1={a1_test}, a5+a6={a5+a6}')

# Test that a1=4 does NOT satisfy (should fail)
seq4 = simulate(4.0)
if abs(seq4[4] + seq4[5] - 1) < 1e-9:
    pass_all = False
    print('FAIL: a1=4 should not satisfy condition')

# Compute answer
M = 2**16
m = 2
answer = math.log2(M / m)
if abs(answer - 15) > 1e-9:
    pass_all = False
    print(f'FAIL: log2(M/m) = {answer}, expected 15')

print('VERIFY_PASS' if pass_all else 'VERIFY_FAIL')
