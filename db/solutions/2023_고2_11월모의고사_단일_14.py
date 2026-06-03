# f(n)을 계산하는 함수
def f(n, m):
    value = m - 2*n
    if n % 2 == 0:  # n이 짝수
        if value > 0:
            return 2
        elif value == 0:
            return 1
        else:
            return 0
    else:  # n이 홀수
        return 1

# 조건을 확인하는 함수
results = []
for m in range(1, 50):
    total = f(2, m) + f(3, m) + f(4, m)
    if total == 3:
        results.append(m)

# 검증
if results == [5, 6, 7] and sum(results) == 18:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')