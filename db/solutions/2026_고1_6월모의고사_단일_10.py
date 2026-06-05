import math

def check_integer_count(a):
    """a값에 대해 부등식 x^2 - 2x - a < 0을 만족하는 정수 개수 반환"""
    count = 0
    for x in range(-10, 10):
        if x*x - 2*x - a < 0:
            count += 1
    return count

# 검증: a = 8일 때
a = 8
count_at_8 = check_integer_count(8)
print(f'a = 8일 때 정수 개수: {count_at_8}')

# 검증: a = 8.0001일 때
a_slightly_larger = 8.0001
count_slightly_larger = check_integer_count(a_slightly_larger)
print(f'a = 8.0001일 때 정수 개수: {count_slightly_larger}')

# 검증: a = 7.9999일 때
a_slightly_smaller = 7.9999
count_slightly_smaller = check_integer_count(a_slightly_smaller)
print(f'a = 7.9999일 때 정수 개수: {count_slightly_smaller}')

if count_at_8 == 5 and count_slightly_larger != 5 and (count_slightly_smaller == 5 or count_slightly_smaller == 3):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')