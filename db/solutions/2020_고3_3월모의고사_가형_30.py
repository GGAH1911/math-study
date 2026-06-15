import sympy as sp
# 최고차4 삼차 f, g(x)=∫_t^x f. f'(a)=0, |g-g(a)| 미분불가점 1개. h(t)=g(a), h(3)=0, h(2)=27(최댓). f(5)?
# f(x)=4(x-a)^2(x-2) (극대계수4, h최대 t=2→f(2)=0→r=2). h(t)=∫_t^a f.
CANDIDATE = 432
s, t, a = sp.symbols('s t a', real=True)
f = 4*(s - a)**2*(s - 2)
h = sp.integrate(f, (s, t, a))                 # h(t)=g(a)
av = [c for c in sp.solve(h.subs(t, 3), a)
      if c.is_real and sp.simplify(h.subs({t: 2, a: c}) - 27) == 0][0]   # h(3)=0 & h(2)=27 → a=-1
f5 = 4*(5 - av)**2*(5 - 2)
print('VERIFY_PASS' if sp.simplify(f5 - CANDIDATE) == 0 else 'VERIFY_FAIL')
