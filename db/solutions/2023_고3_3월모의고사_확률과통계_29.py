import math

# 경우 1: (2, 2, 2)
a1, b1, c1 = 2, 2, 2
sum1 = a1 * 1 + b1 * 2 + c1 * 3
arrange1 = math.factorial(6) // (math.factorial(2) * math.factorial(2) * math.factorial(2))
check1 = (sum1 % 4 == 0) and (a1 >= 1 and b1 >= 1 and c1 >= 1)

# 경우 2: (1, 4, 1)
a2, b2, c2 = 1, 4, 1
sum2 = a2 * 1 + b2 * 2 + c2 * 3
arrange2 = math.factorial(6) // (math.factorial(1) * math.factorial(4) * math.factorial(1))
check2 = (sum2 % 4 == 0) and (a2 >= 1 and b2 >= 1 and c2 >= 1)

# 검증
total = arrange1 + arrange2

if check1 and check2 and sum1 % 4 == 0 and sum2 % 4 == 0 and total == 120:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')