from sympy import symbols, summation
n = symbols('n', integer=True)

# 홀수 항의 합 계산 (n=1,3,5,7,9)
odd_sum = 0
for k in [1, 3, 5, 7, 9]:
    odd_sum += k**2 - 1

# 짝수 항의 합 계산 (n=2,4,6,8,10)
even_sum = 0
for k in [2, 4, 6, 8, 10]:
    even_sum += k**2 + 1

# 전체 합
total = odd_sum + even_sum

if total == 385:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')