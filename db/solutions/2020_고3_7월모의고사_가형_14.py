import sympy as sp
m, s = sp.symbols('m s', positive=True)
# 표준정규 CDF (오차함수 사용, 근사 아님)
def Phi(x):
    return sp.Rational(1,2)*(1+sp.erf(x/sp.sqrt(2)))
# X~N(m,2^2), Y~N(2m,s^2)
eq1 = sp.Eq(Phi((8-m)/2) + Phi((8-2*m)/s), 1)
# P(Y<=m+4)=0.3085 -> 표준화값이 -0.5 (표값 0.3085=0.5-0.1915)
eq2 = sp.Eq((4-m)/s, sp.Rational(-1,2))
sol = sp.solve([eq1, eq2], [m, s], dict=True)
# 양의 sigma 해 선택
cand = [d for d in sol if d[s] > 0 and d[m] > 0]
assert cand, 'no valid solution'
mv = cand[0][m]; sv = cand[0][s]
# 조건 재확인
c1 = sp.simplify(Phi((8-mv)/2)+Phi((8-2*mv)/sv) - 1)
c2 = sp.nsimplify(Phi((mv+4-2*mv)/sv).evalf() - 0.3085)
val = Phi((sv - mv)/2).evalf()  # P(X<=sigma)
# 표값 기반 기대치 0.1587 = 0.5-0.3413
ok = (abs(c1) < 1e-9) and (mv==6) and (sv==4) and (abs(val-0.1587) < 1e-3)
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')
