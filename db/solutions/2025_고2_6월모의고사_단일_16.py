import numpy as np

a_val = -2
b_val = 6

def f(x):
    return a_val * np.sin(np.pi / b_val * x) + a_val**2

# 조건 (가) 검증: 최댓값-최솟값=2
xs = np.linspace(0, b_val, 200000)
f_vals = f(xs)
cond_ga = abs(f_vals.max() - f_vals.min() - 2) < 1e-4

# 조건 (나) 검증: 로그 방정식의 실근 합=6
# f(x)=3 만 유효 (f(x)=2는 진수<0)
def eq(x):
    fx = f(x)
    lhs = fx**2 - 5
    rhs = 5*fx - 11
    return lhs - rhs  # should be 0, and both lhs,rhs>0

g = f(xs) - 3
sign_chg = np.where(np.diff(np.sign(g)))[0]
roots = []
for i in sign_chg:
    x0, x1 = xs[i], xs[i+1]
    g0, g1 = g[i], g[i+1]
    root = x0 - g0*(x1-x0)/(g1-g0)
    # verify domain conditions
    fx = f(root)
    if fx**2 - 5 > 0 and 5*fx - 11 > 0:
        roots.append(root)

sum_roots = sum(roots)
cond_na = abs(sum_roots - 6) < 1e-2

# a+b=4 검증
cond_ans = abs(a_val + b_val - 4) < 1e-9

if cond_ga and cond_na and cond_ans:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: ga={cond_ga}, na={cond_na}(sum={sum_roots:.4f}), ans={cond_ans}')
