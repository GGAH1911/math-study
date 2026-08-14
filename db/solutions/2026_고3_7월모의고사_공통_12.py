# 등비수열(항 양수). a5(a6+a7)=20a10, S4=65 → a2?
import sympy as sp

a, r = sp.symbols('a r', positive=True)
an = lambda n: a*r**(n-1)
S4 = sum(an(i) for i in range(1, 5))
sol = sp.solve([sp.Eq(an(5)*(an(6) + an(7)), 20*an(10)), sp.Eq(S4, 65)], [a, r], dict=True)
sol = [s for s in sol if s[a].is_positive and s[r].is_positive]
val = sp.simplify(an(2).subs(sol[0]))
choices = {1: 12, 2: 14, 3: 16, 4: 18, 5: 20}
pick = [kk for kk, vv in choices.items() if sp.simplify(val - vv) == 0]
print('VERIFY_PASS' if pick == [1] else 'VERIFY_FAIL')
