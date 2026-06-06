import sympy as sp
x = sp.Symbol('x', real=True)
a, b = 7, -1
# 원함수 정의
f_left = -3*x + a            # x <= 1
f_right = (x + b)/(sp.sqrt(x+3) - 2)  # x > 1
# 좌측에서의 함숫값 f(1)
f1 = f_left.subs(x, 1)
# 우극한
right_lim = sp.limit(f_right, x, 1, '+')
# 연속 조건 + a+b 값
cond_cont = sp.simplify(f1 - right_lim) == 0
cond_sum = (a + b) == 6
# 우측에서 x>1 부근 수치검증
import math
def fr(xv):
    return (xv + b)/(math.sqrt(xv+3) - 2)
num_ok = abs(fr(1.0001) - 4) < 1e-3 and abs(fr(1.000001) - 4) < 1e-3
if cond_cont and cond_sum and num_ok:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')