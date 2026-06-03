from sympy import symbols, Eq, solve

# 등차수열 매개변수
a1 = 1
d = 4

# 각 항 계산
a2 = a1 + d
a3 = a1 + 2*d
a5 = a1 + 4*d

# 주어진 조건 검증
condition = a5 - a3
if condition == 8 and a2 == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')