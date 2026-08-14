# AB=10√5 를 지름으로 하는 구 S. C,D 는 S 위, A,B,C,D 는 평면 α 위, AD=BC=10, CD<AB.
# 지름에 대한 원주각이 직각이므로 α∩S 는 AB 를 지름으로 하는 원이고 ∠ADB=∠ACB=π/2.
# (가) P 의 α 정사영이 선분 BD 위 · (나) 평면 PAD 와 α 의 예각이 π/4
# → 평면 PAB 와 평면 PBC 의 예각 θ 에 대해 cos^2θ = q/p, p+q.
CANDIDATE = 52
import sympy as sp

s5 = sp.sqrt(5)
A = sp.Matrix([0, 0, 0]); B = sp.Matrix([10*s5, 0, 0])
D = sp.Matrix([2*s5, 4*s5, 0]); C = sp.Matrix([8*s5, 4*s5, 0])
O = (A + B)/2; R = sp.sqrt((A - O).dot(A - O))
for X, want in ((D, 10), (C, 20)):                      # AD=10, AC=20 확인
    assert sp.simplify(sp.sqrt((X - A).dot(X - A)) - want) == 0
assert sp.simplify(sp.sqrt((C - B).dot(C - B)) - 10) == 0
assert sp.simplify(sp.sqrt((C - D).dot(C - D)) - 6*s5) == 0   # CD=6√5 < AB
for X in (C, D):
    assert sp.simplify(sp.sqrt((X - O).dot(X - O)) - R) == 0  # 구 위

t, z = sp.symbols('t z', positive=True)
F = B + t*(D - B)                                        # 정사영(선분 BD 위)
P = sp.Matrix([F[0], F[1], z])
eq_sphere = sp.Eq((P - O).dot(P - O), R**2)
# 평면 PAD 와 α 의 각: 정사영 F 에서 직선 AD 까지 거리 h 에 대해 tan(π/4)=z/h → z=h
u = (D - A)/sp.sqrt((D - A).dot(D - A))
w = F - A
h = sp.sqrt(sp.simplify(w.dot(w) - w.dot(u)**2))
sol = sp.solve([eq_sphere, sp.Eq(z, h)], [t, z], dict=True)
sol = [s for s in sol if s[t].is_real and 0 < s[t] < 1 and s[z].is_real and s[z] > 0][0]
Pp = P.subs(sol)
n1 = (A - Pp).cross(B - Pp)                              # 평면 PAB
n2 = (B - Pp).cross(C - Pp)                              # 평면 PBC
cos2 = sp.simplify(n1.dot(n2)**2 / (n1.dot(n1)*n2.dot(n2)))
q, p = sp.fraction(sp.nsimplify(cos2))
print('VERIFY_PASS' if sp.Integer(p + q) == CANDIDATE and sp.gcd(p, q) == 1 else 'VERIFY_FAIL')
