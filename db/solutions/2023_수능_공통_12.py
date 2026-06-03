import sympy as sp, itertools
x = sp.symbols('x', real=True)

def f_piece(n_val, eps):
    # |f(x)| = |6(x-n+1)(x-n)|; on [n-1,n) the inside is <=0, so |f|=-6(x-n+1)(x-n).
    return eps * (-6) * (x - n_val + 1) * (x - n_val)

chosen = None
for eps in itertools.product([-1, 1], repeat=4):
    E = {n: eps[n-1] for n in (1,2,3,4)}
    # |f| matches the given formula by construction (eps = ±1).
    I = {n: sp.integrate(f_piece(n, E[n]), (x, n-1, n)) for n in (1,2,3,4)}
    int_0_2 = I[1] + I[2]
    int_0_4 = sum(I.values())
    # g(2) = int_0^2 f - int_2^4 f = 2*int_0^2 f - int_0^4 f, must equal 0.
    if 2*int_0_2 - int_0_4 != 0:
        continue
    # For minimum at x=2: f<=0 on (1,2), f>=0 on (2,3).
    if float(f_piece(2, E[2]).subs(x, sp.Rational(3,2))) > 1e-9: continue
    if float(f_piece(3, E[3]).subs(x, sp.Rational(5,2))) < -1e-9: continue
    # Boundary limits g(0+)=-int_0^4 f, g(4-)=int_0^4 f must both be >=0 => int_0^4 f = 0.
    if int_0_4 != 0: continue
    # Now g(x) = 2*int_0^x f; check g(1), g(3) >= 0 (interior local maxima).
    g1 = 2 * I[1]
    g3 = 2 * (I[1] + I[2] + I[3])
    if g1 < 0 or g3 < 0: continue
    chosen = E
    break

assert chosen is not None, 'no valid sign assignment'
E = chosen
# Numerically confirm g >= 0 on (0,4) with min exactly 0 at x=2.
import numpy as np
def f_num(t):
    n = int(np.floor(t)) + 1
    if n not in E: return 0.0
    return E[n] * (-6) * (t - n + 1) * (t - n)
# crude trapezoidal cumulative integral
ts = np.linspace(0, 4, 40001)
vals = np.array([f_num(t) for t in ts])
cum = np.concatenate([[0], np.cumsum((vals[1:]+vals[:-1])/2 * (ts[1]-ts[0]))])
g_vals = 2*cum - cum[-1]
assert g_vals.min() >= -1e-6
idx2 = np.argmin(np.abs(ts - 2.0))
assert abs(g_vals[idx2]) < 1e-6

# Target integral.
target = sp.integrate(f_piece(1, E[1]), (x, sp.Rational(1,2), 1))
for n in (2,3,4):
    target += sp.integrate(f_piece(n, E[n]), (x, n-1, n))

print('VERIFY_PASS' if target == sp.Rational(-1,2) else f'VERIFY_FAIL target={target}')
