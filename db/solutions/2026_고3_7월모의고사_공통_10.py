# f(x)=cos(πx/a), [0,2a]. y=1/2 과 만나는 점 A,B / y=-1/2 과 만나는 점 C,D.
# 사각형 ACDB(윗변 AB, 아랫변 CD, 높이 1)의 넓이 조건으로 a 를 실제로 풀고 a×AB 판정.
import sympy as sp

a, x = sp.symbols('a x', positive=True)
f = sp.cos(sp.pi*x/a)
xs_up = sorted(sp.solve(sp.Eq(f, sp.Rational(1, 2)), x)[:1] + [2*a - sp.Rational(1, 3)*a])
A, B = a/3, 5*a/3                                  # cos(πx/a)=1/2 → x=a/3, 5a/3
C, D = 2*a/3, 4*a/3                                # cos(πx/a)=-1/2 → x=2a/3, 4a/3
for pt, val in ((A, sp.Rational(1, 2)), (B, sp.Rational(1, 2)),
                (C, -sp.Rational(1, 2)), (D, -sp.Rational(1, 2))):
    assert sp.simplify(f.subs(x, pt) - val) == 0   # 교점이 실제로 맞는지 확인
AB, CD = B - A, D - C
area = sp.Rational(1, 2)*(AB + CD)*1               # 사다리꼴 (높이 = 1/2-(-1/2) = 1)
a0 = sp.solve(sp.Eq(area, sp.Rational(3, 2)), a)[0]
val = sp.simplify((a*AB).subs(a, a0))
choices = {1: sp.Integer(3), 2: sp.Rational(19, 6), 3: sp.Rational(10, 3),
           4: sp.Rational(7, 2), 5: sp.Rational(11, 3)}
pick = [k for k, v in choices.items() if sp.simplify(val - v) == 0]
print('VERIFY_PASS' if pick == [1] else 'VERIFY_FAIL')
