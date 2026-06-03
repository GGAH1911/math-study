import math

# 원래 문제의 조건
lower_bound = 2 - math.sqrt(6)
upper_bound = 5 + math.sqrt(15)

print(f'Lower bound: {lower_bound}')
print(f'Upper bound: {upper_bound}')

# 조건을 만족하는 정수 개수
count = 0
integers = []
for n in range(-10, 20):
    if lower_bound < n < upper_bound:
        count += 1
        integers.append(n)

print(f'Integers satisfying condition: {integers}')
print(f'Count: {count}')

if count == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')