import math
from math import log

# 원래 함수: y = 5^x + 1
def f(x):
    return 5**x + 1

# 역함수: x = log_5(y-1)
def f_inv(y):
    return log(y - 1, 5)

# 답: a = 3
a = 3

# 역함수가 점 (4, log_5(a))를 지나는지 확인
# f_inv(4) = log_5 a 인지 확인
x_on_graph = 4
y_on_graph = log(a, 5)

computed_y = f_inv(x_on_graph)

if abs(computed_y - y_on_graph) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')