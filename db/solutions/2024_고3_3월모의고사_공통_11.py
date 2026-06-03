a6 = -2
d = -5
a1 = a6 - 5*d
seq = [a1 + (k-1)*d for k in range(1, 9)]
sum_a = sum(seq)
sum_abs = sum(abs(x) for x in seq)
if seq[5] == a6 and sum_abs == sum_a + 42 and d < 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')