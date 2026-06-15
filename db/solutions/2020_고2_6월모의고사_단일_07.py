from sympy import *
x = symbols('x', real=True)
f = 2 + (Rational(1, 3))**(2*x)

# 정의역 [-1, 2]에서 최댓값 찾기
f_minus1 = f.subs(x, -1)
f_2 = f.subs(x, 2)

max_val = max(f_minus1, f_2)

if max_val == 11:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')