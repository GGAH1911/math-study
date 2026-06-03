import sympy as sp

t, x = sp.symbols('t x', real=True)

# 원래 문제의 정의 그대로
def f(u):
    return sp.Piecewise((-u**2, u < 0), (u**2 - u, True))

def g(u, a):
    return sp.Piecewise((a*u + a, u < -1), (sp.Integer(0), u < 1), (a*u - a, True))

# 후보 k=4
k = sp.Integer(4)

# (1) k 검증: 영역 1 (x<-1) 에서 h'(x)=x^2+a x+a 가 a=4 에 (x+2)^2 로 인수분해되는지
poly_at_k = sp.expand(g(x, k) - f(x))  # 안 쓰지만 정의가 살아있다는 확인
region1 = x**2 + k*x + k
assert sp.factor(region1) == (x + 2)**2

# a=9/2 (>4) 에서는 영역 1 폴리노미얼이 (-inf,-1) 안에 두 실근을 가짐을 확인
a_pert = sp.Rational(9, 2)
roots = sp.solve(x**2 + a_pert*x + a_pert, x)
real_roots = [r for r in roots if r.is_real]
assert len(real_roots) == 2 and all(r < -1 for r in real_roots)

# 0<a<4 에서는 영역 1 폴리노미얼이 실근 없음 확인
for av in [sp.Rational(1,2), sp.Integer(2), sp.Rational(7,2)]:
    disc = av**2 - 4*av
    assert disc < 0

# (2) h(3) 계산: 원래 식으로 적분 분할
#   [0,1]: g=0, f=t^2-t  =>  integrand = -(t^2-t) = -t^2+t
#   [1,3]: g=4t-4, f=t^2-t  =>  integrand = (4t-4)-(t^2-t) = -t^2+5t-4
h3 = sp.integrate(sp.Integer(0) - (t**2 - t), (t, 0, 1)) \
   + sp.integrate((k*t - k) - (t**2 - t), (t, 1, 3))

answer = k + h3
expected = sp.Rational(15, 2)

if sp.simplify(answer - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
