from sympy import *
k = symbols('k', positive=True, nonzero=True)
a = 2**k
b = 2**(3*k)
# 조건 검증: log_2(a) == log_8(b)
lhs = log(a, 2)
rhs = log(b, 8)
cond = simplify(lhs - rhs)
# log_a(b) 계산
result = simplify(log(b, a))
if cond == 0 and result == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', cond, result)
