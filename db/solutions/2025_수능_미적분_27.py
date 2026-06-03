from sympy import *
x = symbols('x')
# 원래 문제: f(x) = x^3 - 3x^2 + 2x - 1 (최고차항 계수 1인 삼차함수)
def f(v): return v**3 - 3*v**2 + 2*v - 1
def g(v): return f(exp(v)) + exp(v)
# 조건1: g(0)=0 (접선이 x축이므로 점이 x축 위에)
assert simplify(g(0)) == 0, 'g(0) fail'
# 조건1: g'(0)=0 (접선의 기울기=0)
gprime = diff(g(x), x)
assert simplify(gprime.subs(x, 0)) == 0, "g'(0) fail"
# 조건2: g(x) = (e^x - 1)^3 검증
assert simplify(g(x) - (exp(x)-1)**3) == 0, 'g formula fail'
# g(ln3) = 8 확인
assert simplify(g(log(3)) - 8) == 0, 'g(ln3) fail'
# h'(8) = 1/g'(ln3)
val = gprime.subs(x, log(3))
assert simplify(val - 36) == 0, "g'(ln3) fail"
result = Rational(1, 36)
if result == Rational(1, val):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')