import math

# 중복순열: 6개 위치에 a 3개, b 2개, c 1개를 배치
total_positions = 6
a_count = 3
b_count = 2
c_count = 1

# 중복순열 공식
result = math.factorial(total_positions) // (math.factorial(a_count) * math.factorial(b_count) * math.factorial(c_count))

if result == 60:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')