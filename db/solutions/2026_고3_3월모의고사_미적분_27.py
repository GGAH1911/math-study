from sympy import *

n = symbols('n', positive=True, integer=True)

# 조건 2 (만나지 않음) → 하한
L_sq = (n+1)**2 / (n*(3*n+2))
# 조건 1 (두 교점) → 상한
U_sq = n**2 / ((n-1)*(3*n-1))

# a_n^2 > L_sq => 3-1/a_n^2 > 3-1/L_sq (하한)
lower_expr = n * (3 - 1/L_sq)
# a_n^2 < U_sq => 3-1/a_n^2 < 3-1/U_sq (상한)
upper_expr = n * (3 - 1/U_sq)

lim_L = limit(lower_expr, n, oo)
lim_U = limit(upper_expr, n, oo)

# 수치 검증 (n=5000)
n_val = 5000
L_val = (n_val+1)**2 / (n_val*(3*n_val+2))
U_val = n_val**2 / ((n_val-1)*(3*n_val-1))
a_sq = (L_val + U_val) / 2
a = a_sq**0.5
d1 = a*(2*n_val-1)/(a_sq+1)**0.5
d2 = a*(2*n_val+1)/(a_sq+1)**0.5
cond1 = d1 < n_val
cond2 = d2 > n_val+1
lim_val = n_val*(3 - 1/a_sq)

if lim_L == 4 and lim_U == 4 and cond1 and cond2 and abs(lim_val - 4) < 0.01:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: lim_L={lim_L}, lim_U={lim_U}, cond1={cond1}, cond2={cond2}, lim_val={lim_val:.6f}')
