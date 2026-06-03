def a(n):
    return -19 if n % 3 == 0 else 10

n = 29
lhs = sum(a(k) for k in range(1, n+1))
rhs = sum(a(k) for k in range(1, 3*n+1))
if lhs == rhs:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
