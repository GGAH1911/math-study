from math import factorial

# 같은 것이 있는 순열: 6개 문자(a 4개, b 1개, c 1개)를 배열
total_letters = 6
count_a = 4
count_b = 1
count_c = 1

# 경우의 수 = 6! / (4! * 1! * 1!)
result = factorial(total_letters) // (factorial(count_a) * factorial(count_b) * factorial(count_c))

if result == 30:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')