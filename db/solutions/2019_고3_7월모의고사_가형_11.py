import sympy as sp

# k를 변수로 정의
k = sp.Symbol('k', positive=True, real=True)

# f(x)의 점근선: y = k
# f^{-1}(x)의 점근선: x = k
# g(x)의 점근선: x = k^2 + k

# 두 점근선의 교점: (k^2 + k, k)
# 이 점이 y = (1/3)x 위에 있으므로
eq = sp.Eq(k, (k**2 + k) / 3)

# 방정식 풀이
sol = sp.solve(eq, k)
sol = [s for s in sol if s > 0]
k_val = sol[0]

# 검증
x_intersect = k_val**2 + k_val
y_intersect = k_val
y_on_line = x_intersect / 3

if abs(y_intersect - y_on_line) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')