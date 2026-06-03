import math

# 4개 숫자 중 1이 2번, 2가 1번, 3이 1번
# 중복순열: 4! / 2! = 24 / 2 = 12

result = math.factorial(4) // math.factorial(2)
print(f'{result}')
if result == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')