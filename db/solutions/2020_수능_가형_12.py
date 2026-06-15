import sympy as sp

# 2020 수능 가형 12: 밑면 = y=√(e^x/(e^x+1)), x축, y축, x=k 로 둘러싸인 영역.
# x축 수직 단면이 정사각형 → 단면적 = y^2 = e^x/(e^x+1). 부피 = ln7. k?  (보기 ②=ln13)
CANDIDATE = sp.log(13)
x, k = sp.symbols('x k', positive=True)
V = sp.integrate(sp.exp(x) / (sp.exp(x) + 1), (x, 0, k))   # = ln((e^k+1)/2)
kval = [s for s in sp.solve(sp.Eq(V, sp.log(7)), k) if s.is_real][0]
print('VERIFY_PASS' if sp.simplify(kval - CANDIDATE) == 0 else 'VERIFY_FAIL')
