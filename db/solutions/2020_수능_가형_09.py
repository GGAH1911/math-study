import sympy as sp
t = sp.Symbol('t', real=True, positive=True)
dx_dt = 1 + sp.cos(2*t)
dy_dt = sp.sec(t)**2
v_squared = dx_dt**2 + dy_dt**2
v_squared_simplified = 4*sp.cos(t)**4 + 1/sp.cos(t)**4
u = sp.Symbol('u', real=True, positive=True)
f = 4*u**2 + 1/u**2
derivative = sp.diff(f, u)
critical_pts = sp.solve(derivative, u)
u_opt = [cp for cp in critical_pts if 0 < cp < 1][0]
v_min_squared = f.subs(u, u_opt)
v_min = sp.sqrt(v_min_squared)
if v_min == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')