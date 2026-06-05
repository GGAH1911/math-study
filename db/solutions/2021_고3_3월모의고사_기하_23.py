import math

# 타원의 방정식: x^2/36 + y^2/20 = 1
a_squared = 36
b_squared = 20

# c^2 = a^2 - b^2 (a > b일 때 초점은 x축)
c_squared = a_squared - b_squared
c = math.sqrt(c_squared)

# 선분 FF'의 길이 = 2c
length_FF_prime = 2 * c

# 답이 8인지 검증
if abs(length_FF_prime - 8) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')