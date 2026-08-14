# lim (a_n+n^2)/(2n^2+4)=2 → a_n/n^2 → 3. 이를 a_n = 3n^2 + o(n^2) 로 두고 극한을 실제로 계산.
import sympy as sp

n = sp.symbols('n', positive=True)
a = 3*n**2                                    # 조건을 만족하는 대표수열
assert sp.limit((a + n**2)/(2*n**2 + 4), n, sp.oo) == 2
val = sp.limit(1/(sp.sqrt(a + 3*n) - sp.sqrt(a + n)), n, sp.oo)
choices = {1: sp.sqrt(3)/9, 2: sp.Rational(1, 3), 3: sp.sqrt(3)/3, 4: sp.Integer(1), 5: sp.sqrt(3)}
pick = [k for k, v in choices.items() if sp.simplify(val - v) == 0]
print('VERIFY_PASS' if pick == [5] else 'VERIFY_FAIL')
