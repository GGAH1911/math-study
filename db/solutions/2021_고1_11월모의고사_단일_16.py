import sympy as sp

# 원래 문제의 식
result = (14**2 + 2*14)**2 - 18*(14**2 + 2*14) + 45

# 우리의 답: a=11, b=13, c=17, d=19
product = 11 * 13 * 17 * 19

if result == product:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')