from sympy import Rational
a_val = Rational(12)
b_val = Rational(-2)
def f(x_val):
    return a_val / x_val + b_val
# 조건 (가): |f(x)|=2 해 개수
count = 0
if (2 - b_val) != 0:
    count += 1  # x = a/(2-b) = 12/4 = 3
if (-2 - b_val) != 0:
    count += 1  # -2-(-2)=0 → 해 없음, count 증가 안 함
cond_ga = (count == 1)
# 조건 (나)
f_inv_2 = a_val / (2 - b_val)
f2_minus_1 = f(2) - 1
cond_na = (f_inv_2 == f2_minus_1)
# f(8)
f8 = f(8)
if cond_ga and cond_na and f8 == Rational(-1, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')