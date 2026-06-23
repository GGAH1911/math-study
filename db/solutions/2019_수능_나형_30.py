import sympy as sp
# 조건으로 f(x)=x³, g(x)=-(x-2)². x>0서 g(x)<=kx-2<=f(x) 의 k 최대 α·최소 β.
# (A) x³-kx+2>=0(x>0) 경계 → α.  (B) x²+(k-4)x+2>=0(x>0) 경계 → β.
# α-β = a+b√2, a²+b² 구함.
x, k, ks = sp.symbols('x k ks', real=True)
CANDIDATE = 5
# α: h(x)=x³-kx+2 의 x>0 최소(x=√(k/3))가 0 → k
kp = sp.symbols('kp', positive=True)
xc = sp.sqrt(kp/3)
alpha = max([s for s in sp.solve(sp.Eq(xc**3 - kp*xc + 2, 0), kp) if s.is_real and s > 0])
# β: x²+(k-4)x+2 의 판별식 경계(작은 근)
beta = min(sp.solve(sp.Eq(2 - (k-4)**2/4, 0), k))
diff = sp.expand(alpha - beta)            # a + b√2
a = diff.subs(sp.sqrt(2), 0)              # 유리수부
b = sp.simplify((diff - a)/sp.sqrt(2))    # √2 계수
val = sp.nsimplify(a**2 + b**2)
print('VERIFY_PASS' if val == CANDIDATE else 'VERIFY_FAIL')
