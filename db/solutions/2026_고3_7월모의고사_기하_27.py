# α 위에서 A 에서 직교하는 두 직선 l, m. P 에서 l, m 에 내린 수선의 발이 B, C.
# A 를 원점, l 을 x축, m 을 y축, α 를 z=0 으로 두면 B=(b,0,0), C=(0,c,0) 이고
# P 의 수선의 발이 B, C 이므로 P=(b,c,h). AB=2√3, AC=2, PA=5 로 h 를 실제로 푼다.
# 삼각형 ABC 의 평면 PBC 위로의 정사영 넓이 = |ABC| · cos(두 평면이 이루는 각).
import sympy as sp

h = sp.symbols('h', positive=True)
b, c = 2*sp.sqrt(3), sp.Integer(2)
A = sp.Matrix([0, 0, 0]); B = sp.Matrix([b, 0, 0]); C = sp.Matrix([0, c, 0])
h0 = sp.solve(sp.Eq(b**2 + c**2 + h**2, 5**2), h)[0]
P = sp.Matrix([b, c, h0])
n1 = (B - A).cross(C - A)                       # 평면 ABC 의 법선
n2 = (B - P).cross(C - P)                       # 평면 PBC 의 법선
cos = sp.Abs(n1.dot(n2)) / (n1.norm() * n2.norm())
area_ABC = sp.Rational(1, 2) * n1.norm()
proj = sp.simplify(area_ABC * cos)
choices = {1: sp.sqrt(3)/3, 2: sp.sqrt(6)/2, 3: sp.sqrt(3), 4: 2*sp.sqrt(2), 5: 4*sp.sqrt(6)/3}
pick = [k for k, v in choices.items() if sp.simplify(proj - v) == 0]
print('VERIFY_PASS' if pick == [3] else 'VERIFY_FAIL')
