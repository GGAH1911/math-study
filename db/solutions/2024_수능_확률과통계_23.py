import math

# 같은 것이 있는 순열: 5개 중 x 2개, y 2개, z 1개
total = 5
x_count = 2
y_count = 2
z_count = 1

# 공식: n! / (n1! * n2! * n3!)
result = math.factorial(total) // (math.factorial(x_count) * math.factorial(y_count) * math.factorial(z_count))

if result == 30:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')