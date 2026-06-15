import sympy as sp

# 2020 수능 가형 30: y=t^3 ln(x-t) 와 y=2e^{x-a} 가 오직 한 점에서 만나는 a=f(t). {f'(1/3)}^2?
# 접점 x0: g=t^3 ln(x0-t)-2e^{x0-a}=0, g'=t^3/(x0-t)-2e^{x0-a}=0
# → ln u0 = 1/u0 (u0=x0-t, t와 무관한 상수).  a = x0 - 3 ln t + ln(2 u0) = t+u0-3 ln t+ln(2u0).
CANDIDATE = 64
t, u0 = sp.symbols('t u0', positive=True)   # u0: t에 무관한 상수
f = t + u0 - 3 * sp.log(t) + sp.log(2 * u0)  # a = f(t)
fp = sp.diff(f, t)                           # f'(t) = 1 - 3/t  (u0항 소거)
val = (fp.subs(t, sp.Rational(1, 3)))**2     # {f'(1/3)}^2 = (-8)^2
print('VERIFY_PASS' if sp.simplify(val - CANDIDATE) == 0 else 'VERIFY_FAIL')
