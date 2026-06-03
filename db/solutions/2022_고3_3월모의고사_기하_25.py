import sympy as sp

x, y = sp.symbols('x y', real=True)
F = 4*x**2 - 8*x - y**2 - 6*y - 9  # 원래 쌍곡선 식

# y에 대해 풀어 두 가지(branch)를 얻고, x→∞ 점근선의 기울기·절편 구하기
ys = sp.solve(F, y)
slopes = [sp.simplify(sp.limit(yi/x, x, sp.oo)) for yi in ys]
intercepts = [sp.simplify(sp.limit(yi - s*x, x, sp.oo)) for yi, s in zip(ys, slopes)]

# 기울기가 양수인 점근선 선택
pos_idx = None
for i, s in enumerate(slopes):
    if s.is_real and s > 0:
        pos_idx = i
        break
assert pos_idx is not None
m = slopes[pos_idx]
c = intercepts[pos_idx]  # y = m x + c

# 그 점근선이 실제로 쌍곡선 위 점들의 극한임을 확인 (큰 x에서 잔차→0)
residual = sp.limit(ys[pos_idx] - (m*x + c), x, sp.oo)
assert sp.simplify(residual) == 0

# x축, y축과의 교점
x_int = sp.solve(m*x + c, x)[0]      # y=0
y_int = c                             # x=0

area = sp.Rational(1, 2) * sp.Abs(x_int) * sp.Abs(y_int)
expected = sp.Rational(25, 4)

if sp.simplify(area - expected) == 0 and m == 2 and sp.simplify(c + 5) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
