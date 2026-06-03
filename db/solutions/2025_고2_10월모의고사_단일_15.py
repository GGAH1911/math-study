def f(n):
    val = n - 12
    if n % 2 == 1:  # n이 홀수
        return 1
    else:  # n이 짝수
        if val > 0:
            return 2
        elif val == 0:
            return 1
        else:
            return 0

valid_n = []
for n in range(2, 30):
    if f(n) + f(2*n) == 1:
        valid_n.append(n)

result = sum(valid_n)
if result == 14:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')