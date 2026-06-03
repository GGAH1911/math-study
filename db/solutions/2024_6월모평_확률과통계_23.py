import math

# 5개 문자: a, a, b, c, d
# 같은 것이 있는 순열: 5! / 2!

total_permutations = math.factorial(5)
a_count_factorial = math.factorial(2)  # a가 2개

result = total_permutations // a_count_factorial

if result == 60:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')