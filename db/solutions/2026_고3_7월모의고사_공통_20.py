# 등차수열 {a_n}, b_n = 2(S_n - n a_n) (n 홀수) / (n-1)a_n (n 짝수), b_2 = 2.
# (가) f(k), (나) g(k), (다) p 를 실제로 유도해 f(2)+g(3)+p 를 구한다.
CANDIDATE = 213
import sympy as sp

k, n, a1, d = sp.symbols('k n a1 d')
a = lambda i: a1 + (i - 1)*d
S = lambda i: sp.simplify(i*(a1 + a(i))/2)
b_odd = sp.simplify(2*(S(2*k - 1) - (2*k - 1)*a(2*k - 1)))
f_k = sp.simplify(sp.cancel(b_odd/(a1 - a(2*k - 1))))        # (가)
b_even = sp.simplify((2*k - 1)*a(2*k))
g_k = sp.simplify(sp.expand(b_odd + b_even))                  # (나) — a2=2 대입 전
a2_val = sp.solve(sp.Eq(a(2), 2), a1)[0]                      # b_2 = (2-1)a_2 = 2 → a_2 = 2
g_k = sp.simplify(g_k.subs(a1, a2_val))
p = sp.simplify(sp.summation(g_k, (k, 1, 10)))                # (다)
val = sp.simplify(f_k.subs(k, 2) + g_k.subs(k, 3) + p)
print('VERIFY_PASS' if sp.simplify(val - CANDIDATE) == 0 else 'VERIFY_FAIL')
