import sympy as sp

x = sp.Symbol('x')
f = sp.tan(2*x) + sp.pi/2

# 점 P의 좌표
x_p = sp.pi/8
y_p = f.subs(x, x_p)
y_p = sp.simplify(y_p)

# 기울기
f_prime = sp.diff(f, x)
m = f_prime.subs(x, x_p)
m = sp.simplify(m)

# 접선의 y절편: y = m(x - x_p) + y_p에서 x=0
y_intercept = y_p - m * x_p
y_intercept = sp.simplify(y_intercept)

# 검증
if y_intercept == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')