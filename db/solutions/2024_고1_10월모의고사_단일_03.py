from sympy import *

# 문제 조건
U = {1, 2, 3, 4, 5}
A = {1, 3, 5}

# A^C 계산
A_complement = U - A

# 모든 원소의 곱
product = 1
for elem in A_complement:
    product *= elem

# 내 답
my_answer = 8

if product == my_answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')