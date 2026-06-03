import sympy as sp
import numpy as np

c = 3*sp.sqrt(6)/2
t = sp.symbols('t', real=True)
# Original problem: P on line y=2x-3, A=(c,0), B=(-c,0)
PA = sp.sqrt((t - c)**2 + (2*t - 3)**2)
PB = sp.sqrt((t + c)**2 + (2*t - 3)**2)
f = PB - PA

# Check P=(3,3) is on the line
assert 3 == 2*3 - 3

# Check derivative is zero at t=3 (critical point)
df = sp.diff(f, t)
val_deriv = sp.simplify(df.subs(t, 3))

# Numerical check: t=3 truly maximizes f(t) along the line
c_val = float(c)
def f_num(tt):
    return (np.sqrt((tt + c_val)**2 + (2*tt - 3)**2)
            - np.sqrt((tt - c_val)**2 + (2*tt - 3)**2))

ts = np.linspace(-100, 100, 200001)
vals = f_num(ts)
fmax = float(np.max(vals))
f3 = float(f_num(3.0))
argmax_t = float(ts[int(np.argmax(vals))])

ok_deriv = (val_deriv == 0)
ok_global_max = (abs(fmax - f3) < 1e-4) and (abs(argmax_t - 3.0) < 0.01)

if ok_deriv and ok_global_max:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
