import sympy as sp

# 원래 문제의 조건을 직접 검증
a = sp.symbols('a', real=True, nonzero=True)
bx, by, cx, cy = sp.symbols('bx by cx cy', real=True)
Ax, Ay = 2*a, 0

eqs = [
    (Ax + bx + cx) - 0,                                       # 무게중심 x = 0 (×3)
    (Ay + by + cy) - 6,                                       # 무게중심 y = 2 (×3)
    (bx-Ax)**2 + (by-Ay)**2 - ((cx-Ax)**2 + (cy-Ay)**2),      # AB = AC
    (bx-cx)**2 + (by-cy)**2 - 4*(a**2+1),                     # BC = 2*sqrt(a^2+1)
]
sols = sp.solve(eqs, [bx, by, cx, cy], dict=True)

# B_x > C_x 인 해를 선택
chosen = None
for s in sols:
    diff = sp.simplify(s[bx] - s[cx])
    # diff가 양수가 되는 해
    if sp.simplify(diff - 2) == 0:
        chosen = s
        break
assert chosen is not None, 'no valid solution'

B_x = sp.simplify(chosen[bx])  # 1 - a
B_y = sp.simplify(chosen[by])  # a + 3
M_y = sp.simplify((chosen[by] + chosen[cy]) / 2)  # 3 = (가)
sum_B = sp.simplify(B_x + B_y)  # 4 = (라)

# 직선 BC 기울기 (나)
slope_BC = sp.simplify((chosen[by] - chosen[cy]) / (chosen[bx] - chosen[cx]))  # a

# (가)=3=p, (나)=a=f(a), (다)=1-a=g(a), (라)=4=q
p = M_y          # 3
q = sum_B        # 4
f = lambda x: slope_BC.subs(a, x)   # f(a)=a → f(p)=p
g = lambda x: B_x.subs(a, x)        # g(a)=1-a → g(q)=1-q

result = sp.simplify(f(p) * g(q))

if p == 3 and q == 4 and sp.simplify(slope_BC - a) == 0 and sp.simplify(B_x - (1-a)) == 0 and result == -9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
