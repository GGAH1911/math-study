from sympy import symbols, diff, solve

# 2020 6월모평 나형 27: f(x)=x^3+3x^2-k, g(x)=2x^2+3x-10.
# f(x) >= 3 g(x) 가 [-1,4] 에서 항상 성립하게 하는 k 의 최댓값?
# f-3g = x^3-3x^2-9x+30-k >= 0  ⟺  k <= h(x)=x^3-3x^2-9x+30  (모든 x∈[-1,4])
# ⟹ k_max = min_{[-1,4]} h
CANDIDATE = 3
x = symbols('x')
h = x**3 - 3*x**2 - 9*x + 30
crit = [c for c in solve(diff(h, x), x) if c.is_real and -1 <= c <= 4]
hmin = min(h.subs(x, p) for p in crit + [-1, 4])
print('VERIFY_PASS' if hmin == CANDIDATE else 'VERIFY_FAIL')
