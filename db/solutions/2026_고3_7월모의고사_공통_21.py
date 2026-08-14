# f 는 [a, 1.5a] 에서 (x-a)(x-4), 그 밖에서 (x-a)(x-b) 인 조각함수 (a,b>0).
# g(t)=|f(x)|=t 의 서로 다른 실근 개수.
# (가) t→0+ 에서 6 → f 의 단순영점이 3개: x=a, x=4(8/3≤a≤4), x=b(b<a) 여야 한다.
# (나) 불연속이 α, β 둘뿐이고 t→α+ 와 t→β- 에서 1 → g 는 6 → 1 → 2 로 떨어진다.
#   · α 에서 5개가 한꺼번에 사라지려면 두 봉우리 높이가 같고( ((4-a)/2)^2 = ((a-b)/2)^2 )
#     x=1.5a 의 점프도 같은 높이를 지나야 한다( |f(1.5a^-)| = α ).
#   · β 는 x>1.5a 쪽 가지가 처음 t 에 닿는 높이 f(1.5a^+).
# 이 조건들을 실제로 풀어 a,b 를 구하고 f(0)=ab 를 p+q√2 로 분해한다.
CANDIDATE = 320
import sympy as sp

a = sp.symbols('a', positive=True)
b = 2*a - 4                                   # 봉우리 높이 같음: (4-a)=(a-b)
alpha = ((4 - a)/2)**2                        # [a,1.5a] 조각의 봉우리
left_end = sp.simplify((sp.Rational(3, 2)*a - a)*(sp.Rational(3, 2)*a - 4))   # f(1.5a^-)
a0 = [s for s in sp.solve(sp.Eq(sp.Abs(left_end), alpha), a)
      if s.is_real and sp.Rational(8, 3) <= s <= 4]
a0 = a0[0]
b0 = sp.simplify(b.subs(a, a0))
assert b0 > 0 and b0 < a0                     # (가) 의 b<a 조건
f0 = sp.expand(sp.simplify(a0*b0))            # f(0) = (0-a)(0-b) = ab
p, q = f0.as_independent(sp.sqrt(2), as_Add=True)
q = sp.simplify(q/sp.sqrt(2))
val = sp.simplify(p**2 + q**2)
print('VERIFY_PASS' if sp.simplify(val - CANDIDATE) == 0 else 'VERIFY_FAIL')
