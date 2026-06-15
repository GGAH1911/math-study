import sympy as sp
# 내접삼각형 ABC, AB=6, cosα=3/4 (∠ABC). D는 호BC 위, S1:S2=9:5 → AD=6BC/5, DC=4, ∠ADC=α.
# 코사인법칙 ABC=ADC 로 BC 결정 → S=½·AD·DC·sinα. S²?
CANDIDATE = 63
BC = sp.symbols('BC', positive=True)
cosa = sp.Rational(3, 4); sina = sp.sqrt(1 - cosa**2)
AB, DC = 6, 4
AD = sp.Rational(6, 5) * BC
eq = sp.Eq(AB**2 + BC**2 - 2*AB*BC*cosa, AD**2 + DC**2 - 2*AD*DC*cosa)  # AC² 두 표현
bcv = [r for r in sp.solve(eq, BC) if r > 0][0]                          # BC=5
S = sp.Rational(1, 2) * AD.subs(BC, bcv) * DC * sina                      # △ADC 넓이 = 3√7
print('VERIFY_PASS' if sp.simplify(S**2 - CANDIDATE) == 0 else 'VERIFY_FAIL')
