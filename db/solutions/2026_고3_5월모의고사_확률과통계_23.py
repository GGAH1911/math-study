from math import factorial

# 7개의 문자: a 3개, b 3개, c 1개
n = 7
count_a = 3
count_b = 3
count_c = 1

# 중복순열: n! / (n1! * n2! * n3!)
result = factorial(n) // (factorial(count_a) * factorial(count_b) * factorial(count_c))

# 검증: 답이 140인지 확인
if result == 140:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')