def f(x, y):
    return y // 3 if y % 3 == 0 else x + y

def gen(a1, a2, n=9):
    a = [a1, a2]
    for i in range(2, n):
        a.append(f(a[i-2], a[i-1]))
    return a

# Sequences achieving M=200 and m=24
seq_max = gen(1, 3239)   # expect a_9 = 200
seq_min = gen(71, 1)     # expect a_9 = 24
seq_mid = gen(269, 1)    # expect a_9 = 90 (intermediate case)

# Check all three satisfy a_7 = 40
assert seq_max[6] == 40 and seq_min[6] == 40 and seq_mid[6] == 40
assert seq_max[8] == 200
assert seq_min[8] == 24
assert seq_mid[8] == 90

# Confirm no other a_9 values via case analysis: a_6 must satisfy
#   - case A: a_6 = 120
#   - case B1: a_6 = 10
#   - case B2: a_6 = 32
# leading to a_9 in {200, 90, 24}.
# Brute-force small-range sanity check.
found = set()
for a1 in range(1, 400):
    for a2 in range(1, 400):
        s = gen(a1, a2)
        if s[6] == 40:
            found.add(s[8])
found.update({24, 90, 200})  # include constructions outside small range

if not found.issubset({24, 90, 200}):
    print('VERIFY_FAIL')
elif max(found) == 200 and min(found) == 24 and 200 + 24 == 224:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
