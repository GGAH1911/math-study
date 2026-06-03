def nxt(a):
    if a % 3 == 0:
        return a // 3
    else:
        v = a*a + 5
        assert v % 3 == 0
        return v // 3

valid = []
for a1 in range(1, 100000):
    a = a1
    seq = [a]
    for _ in range(4):
        a = nxt(a)
        seq.append(a)
    if seq[3] + seq[4] == 5:
        valid.append(a1)

print('valid a1 =', valid, 'sum =', sum(valid))
if sum(valid) == 72 and set(valid) == {2,7,9,54}:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')