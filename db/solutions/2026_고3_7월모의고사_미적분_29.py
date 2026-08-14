# 등비수열 a_n=a r^{n-1} (수렴 → |r|<1). b_n 정의와 조건 (가)a_n b_n<0 에서 a>0, -1<r<0 이 강제된다.
# 조건 (나) (Σ|a_n|)^2 = 2 Σ a_n^2 로 r 을 실제로 풀고, Σ(a_n+b_n)=63 으로 a 를 푼 뒤 Σ b_{2n} 을 구한다.
CANDIDATE = 30
import sympy as sp

a, r, k = sp.symbols('a r k', positive=True)
rr = sp.symbols('rr', negative=True)
S_abs = a/(1 - sp.Abs(rr))                                   # Σ|a_n| (|rr|=-rr)
S_sq = a**2/(1 - rr**2)                                      # Σ a_n^2
r0 = sp.solve(sp.Eq((a/(1 + rr))**2, 2*S_sq), rr)
r0 = [x for x in r0 if x.is_real and -1 < x < 0][0]           # -1/3
# b_n: n 홀수 → b_n=a_{2n}=a r^{2n-1}, n 짝수 → b_n=-a_n
Sb_odd = sp.summation(a*r0**(4*k - 3), (k, 1, sp.oo))        # n=2k-1
Sb_even = sp.summation(-a*r0**(2*k - 1), (k, 1, sp.oo))      # n=2k
Sa = a/(1 - r0)
a0 = sp.solve(sp.Eq(sp.simplify(Sa + Sb_odd + Sb_even), 63), a)[0]
val = sp.simplify(Sb_even.subs(a, a0))                        # Σ b_{2n}
print('VERIFY_PASS' if sp.simplify(val - CANDIDATE) == 0 else 'VERIFY_FAIL')
