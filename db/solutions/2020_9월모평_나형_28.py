import sympy as sp

# 2020 9월모평 나형 28: 양수 a,b,c,k. (가) 3^a=5^b=k^c  (나) log c = log(2ab)-log(2a+b). k^2?
# (가) 공통값 m, L=ln m: a=L/ln3, b=L/ln5, c=L/ln k.   (나) c = 2ab/(2a+b).
CANDIDATE = 75
L, lk = sp.symbols('L lk', positive=True)   # L=ln m, lk=ln k
ln3, ln5 = sp.log(3), sp.log(5)
a = L / ln3
b = L / ln5
c = L / lk
sol_lk = sp.solve(sp.Eq(c, 2 * a * b / (2 * a + b)), lk)[0]
k2 = sp.exp(2 * sol_lk)                       # k^2 = exp(2 ln k)
print('VERIFY_PASS' if sp.simplify(k2 - CANDIDATE) == 0 else 'VERIFY_FAIL')
