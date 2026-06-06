import sympy as sp
x, a, b = sp.symbols('x a b', real=True)

# Case 1 검증
f1 = a*(x+3)*(x-2)
g1 = b*(x+2)*(x-3)

# ㄱ 검증: f(2)=0일 때 g(3)=0
f1_at_2 = f1.subs(x, 2)
g1_at_3 = g1.subs(x, 3)
print('ㄱ 검증:', 'VERIFY_PASS' if f1_at_2==0 and g1_at_3==0 else 'VERIFY_FAIL')

# ㄴ 검증: ab=1, b<0일 때
ab_constraint = a*b - 1
f1_at_5_2 = f1.subs(x, sp.Rational(5,2))
g1_at_5_2 = g1.subs(x, sp.Rational(5,2))
# b<0, a<0이면 f(5/2)<0, g(5/2)>0
test_b_neg = g1_at_5_2.subs(b, -1).subs(a, -1)
test_f = f1_at_5_2.subs(a, -1)
print('ㄴ 검증:', 'VERIFY_PASS' if test_f<0 and test_b_neg>0 else 'VERIFY_FAIL')

# ㄷ 검증: 정수근 조건
a_sq = sp.Rational(2,3)
eq = (a_sq-1)*x**2 + (a_sq+1)*x - 6*(a_sq-1)
roots = sp.solve(eq, x)
m_plus_n = sum(roots)
print('ㄷ 검증:', 'VERIFY_PASS' if abs(m_plus_n)==5 else 'VERIFY_FAIL')