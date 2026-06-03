import math
from math import cos, sin, exp, pi

# 원래 피적분함수
f = lambda x: cos(x - pi/4) * exp(sin(x - pi/4))

# 심슨 공식으로 수치 적분
a, b = pi/4, 3*pi/4
N = 100000
h = (b - a) / N
s = f(a) + f(b)
for i in range(1, N):
    x = a + i*h
    s += (4 if i % 2 == 1 else 2) * f(x)
numeric = s * h / 3

my_answer = math.e - 1
if abs(numeric - my_answer) < 1e-8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print('numeric=', numeric, 'my=', my_answer)
