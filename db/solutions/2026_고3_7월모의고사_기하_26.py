# 타원 x^2/48 + y^2/(4b^2)=1 위의 P(6,b) 에서의 접선이 x,y축과 만나는 점 A,B.
# PF+PF' = 장축 2a = 8√3 이고 이것이 AB 와 같다는 조건으로 b 를 실제로 푼다.
import sympy as sp

b, x, y = sp.symbols('b x y', positive=True)
assert sp.simplify(sp.Rational(36, 48) + b**2/(4*b**2) - 1) == 0      # P 가 타원 위
tangent = sp.Eq(6*x/48 + b*y/(4*b**2), 1)                              # 접선
A = sp.solve(tangent.subs(y, 0), x)[0]                                 # x절편
B = sp.solve(tangent.subs(x, 0), y)[0]                                 # y절편
AB = sp.sqrt(A**2 + B**2)
b2 = sp.solve(sp.Eq(2*sp.sqrt(48), AB), b)[0]**2                       # PF+PF' = 2a
c = sp.sqrt(48 - 4*b2)
val = sp.simplify(b2*c)
choices = {1: 20, 2: 24, 3: 28, 4: 32, 5: 36}
pick = [k for k, v in choices.items() if sp.simplify(val - v) == 0]
print('VERIFY_PASS' if pick == [4] else 'VERIFY_FAIL')
