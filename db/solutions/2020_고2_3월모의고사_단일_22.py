import math

CANDIDATE = 6

# $_3P_2$ 계산
result = math.factorial(3) // math.factorial(3 - 2)

if result == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')