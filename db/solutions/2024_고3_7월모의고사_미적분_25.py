import sympy as sp
from sympy import symbols, sqrt, limit, oo, Rational, simplify

n = symbols('n', positive=True)
# 조건 lim a_n*(sqrt(n^2+4)-n) = 6 을 만족하는 양수 수열 a_n 의 점근형
# 일반형: a_n = 3n + b_n,  b_n/n -> 0 (조건과 양립)
# 여러 가지 b_n 으로 답이 일정한지 확인

answer_candidates = []
for bn in [sp.Integer(0), sp.Rational(7,1), sp.sqrt(n), sp.log(n+1), 1/n, n**sp.Rational(1,3)]:
    a_n = 3*n + bn
    cond = limit(a_n*(sqrt(n**2+4)-n), n, oo)
    target = limit((2*a_n + 6*n**2)/(n*a_n + 5), n, oo)
    answer_candidates.append((simplify(cond), simplify(target)))

# 조건이 6 이고 목표 극한이 2 인지 확인
ok = all(c == 6 and t == 2 for c, t in answer_candidates)
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')
