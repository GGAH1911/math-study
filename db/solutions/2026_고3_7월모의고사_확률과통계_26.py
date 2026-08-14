# X~N(m,σ^2). P(m≤X≤2m)=0.4772 → (2m-m)/σ=2 ; P(X≥2)=0.8413 → (2-m)/σ=-1.
# 두 식을 실제로 풀어 m,σ 를 구하고 P(0≤X≤5) 를 표 값으로 조립한다.
import sympy as sp

m, s = sp.symbols('m s', positive=True)
sol = sp.solve([sp.Eq((2*m - m)/s, 2), sp.Eq((2 - m)/s, -1)], [m, s], dict=True)[0]
m0, s0 = sol[m], sol[s]
z_lo = sp.simplify((0 - m0)/s0)                 # -2
z_hi = sp.simplify((5 - m0)/s0)                 # 0.5
table = {sp.Rational(1, 2): sp.Rational(1915, 10000), sp.Integer(1): sp.Rational(3413, 10000),
         sp.Rational(3, 2): sp.Rational(4332, 10000), sp.Integer(2): sp.Rational(4772, 10000)}
val = table[abs(z_lo)] + table[z_hi]
choices = {1: sp.Rational(5328, 10000), 2: sp.Rational(6247, 10000), 3: sp.Rational(6687, 10000),
           4: sp.Rational(6826, 10000), 5: sp.Rational(7745, 10000)}
pick = [k for k, v in choices.items() if sp.simplify(val - v) == 0]
print('VERIFY_PASS' if pick == [3] else 'VERIFY_FAIL')
