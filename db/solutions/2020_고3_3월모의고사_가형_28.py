CANDIDATE = 40

from sympy import *

a = Rational(1, 3)
b = Integer(1)

x = symbols('x')
f = 2*sin(a*x) + b

# 점 A(-pi/2, 0) 대입
val_A = f.subs(x, -pi/2)
# 점 B(7pi/2, 0) 대입
val_B = f.subs(x, 7*pi/2)

# 조건 검증
cond_A = simplify(val_A) == 0
cond_B = simplify(val_B) == 0
cond_range = (0 < a) and (a < Rational(4, 7))
cond_rational_b = b.is_rational

# 30(a+b) 계산
result = 30*(a + b)
cond_result = result == CANDIDATE

if cond_A and cond_B and cond_range and cond_rational_b and cond_result:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'val_A={val_A}, val_B={val_B}, result={result}, CANDIDATE={CANDIDATE}')
