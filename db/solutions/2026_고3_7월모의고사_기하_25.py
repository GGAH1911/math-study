# 점 (3√2,0) 을 지나고 방향 u=(1,2√2) 인 직선 위 P 에 대한 |OP| 의 최솟값 = 원점-직선 거리.
# 보기: ①8/3 ②3 ③10/3 ④11/3 ⑤4  → 최솟값을 실제로 구해 어느 보기와 같은지 판정.
import sympy as sp

t = sp.symbols('t', real=True)
P = sp.Matrix([3*sp.sqrt(2) + t, 2*sp.sqrt(2)*t])
d2 = sp.expand(P.dot(P))
t0 = sp.solve(sp.diff(d2, t), t)[0]            # 최소 지점
mn = sp.simplify(sp.sqrt(d2.subs(t, t0)))
choices = {1: sp.Rational(8, 3), 2: sp.Integer(3), 3: sp.Rational(10, 3),
           4: sp.Rational(11, 3), 5: sp.Integer(4)}
pick = [k for k, v in choices.items() if sp.simplify(mn - v) == 0]
print('VERIFY_PASS' if pick == [5] else 'VERIFY_FAIL')
