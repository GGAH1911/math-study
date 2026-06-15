import sympy as sp

# 2020 수능 가형 26: f(x)=(x^2+2)e^{-x}. g 미분가능, g((x+8)/10)=f^{-1}(x), g(1)=0. |g'(1)|?
# x=2 에서 (x+8)/10=1, f(0)=2 → f^{-1}(2)=0=g(1).  양변 미분:
# g'((x+8)/10)*(1/10) = (f^{-1})'(x) = 1/f'(f^{-1}(x)).  x=2: g'(1)/10 = 1/f'(0).
CANDIDATE = 5
x = sp.symbols('x')
f = (x**2 + 2) * sp.exp(-x)
fp0 = sp.diff(f, x).subs(x, 0)        # f'(0) = -2
gp1 = 10 * (1 / fp0)                   # g'(1) = -5
print('VERIFY_PASS' if sp.Abs(gp1) == CANDIDATE else 'VERIFY_FAIL')
