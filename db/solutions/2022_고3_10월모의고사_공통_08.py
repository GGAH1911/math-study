from sympy import symbols, Abs

# 원래 점화식으로 수열 계산
a = {1: 20}
for n in range(1, 30):
    a[n+1] = abs(a[n]) - 2

# 처음 30항의 합
total_sum = sum(a[n] for n in range(1, 31))

if total_sum == 90:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')