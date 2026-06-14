import sympy as sp
x = sp.symbols('x')
# 그래프 판독값을 식으로 표현
# 오른쪽 가지(x>2): (2,3)에 열린 원을 갖는 매끄러운 곡선(아래로 볼록 포물선, 꼭짓점 (3,15/4), (2,3) 통과)
f_right = sp.Rational(-3,4)*(x-3)**2 + sp.Rational(15,4)
right_limit = sp.limit(f_right, x, 2, dir='+')  # x->2+ 우극한 = 3
# f(-1): (-1,1)의 닫힌 점
f_minus1 = sp.Integer(1)
result = f_minus1 + right_limit
CANDIDATE = 4
if sp.simplify(result - CANDIDATE) == 0 and right_limit == 3 and f_minus1 == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
