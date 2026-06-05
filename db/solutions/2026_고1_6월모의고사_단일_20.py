count = 0
for m in [-5,-4,-3,-2,-1,1,2,3,4,5]:
    for n in range(1,11):
        if n == 3:
            continue
        lo, hi = min(n,3), max(n,3)
        sols = [x for x in range(lo+1, hi) if (m*x - 3)*(x + m) >= 0]
        if len(sols) == 1:
            count += 1
print('count =', count)
print('VERIFY_PASS' if count == 20 else 'VERIFY_FAIL')