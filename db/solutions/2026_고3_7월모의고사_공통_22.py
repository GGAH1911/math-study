# 곡선1 y=2^{x-m}+n 위의 A(a,b) (a<b, 제1사분면), B 는 A 를 y=x 에 대칭시킨 점 (b,a).
# B 중심 반지름 5√2 인 원과 곡선2 y=log_2(x-n+1)+m-7 의 교점 중 x 가 작은 점이 C.
# (가) AC ⊥ (y=x/3) → AC 의 기울기 -3.   (나) [AOB]:[ACB] = 27:8.
#   [AOB]=½|a-b||a+b|,  (가) 를 쓰면 [ACB]=|a-b||c-a| → 비 = |a+b| / (2|c-a|) = 27/8.
# 미지수는 (a,c) 둘인데 식이 셋이라 (m,n) 이 특정된다 → 자연수 (m,n) 을 훑어 최댓값을 찾는다.
# ★로그 정의역을 벗어나면 복소수가 되므로 c = n-1+2^u 로 치환해 정의역 안에서만 푼다.
CANDIDATE = 26
import mpmath as mp
import sympy as sp

mp.mp.dps = 15   # 게이트 제한(40s) 안에 끝나야 한다
TARGET = mp.mpf(27)/8

def solve_mn(m, n):
    f = lambda x: mp.power(2, x - m) + n
    def sys(a, u):
        c = n - 1 + mp.power(2, u); b = f(a); yC = u + m - 7
        return (yC - (b - 3*(c - a)), (c - b)**2 + (yC - a)**2 - 50)
    out = []
    for a0 in [m, m+2, m+4]:
        for u0 in [0, 2, 4]:
            try: a, u = mp.findroot(sys, (mp.mpf(a0), mp.mpf(u0)), tol=1e-14)
            except Exception: continue
            a, u = mp.re(a), mp.re(u)
            c, b = n - 1 + mp.power(2, u), f(a)
            if not (a > 0 and a < b and abs(c - a) > 1e-9): continue
            if abs(abs(a + b)/(2*abs(c - a)) - TARGET) < 1e-7:
                out.append((a, c))
    return out

# m,n 은 자연수. 범위는 넉넉히 두되 게이트 시간 안에 끝나도록 20 까지 훑는다
ok_pairs = [(m, n) for m in range(1, 21) for n in range(1, 21) if solve_mn(m, n)]
best = max(m + n for m, n in ok_pairs)
m0, n0 = max(ok_pairs, key=lambda t: t[0] + t[1])

# ★찾은 (m,n) 을 sympy 로 다시 확인 — 세 조건이 정말 동시에 성립하는지 식으로 푼다.
a, c = sp.symbols('a c', real=True)
b = 2**(a - m0) + n0
yC = sp.log(c - n0 + 1, 2) + m0 - 7
eqs = [sp.Eq(yC - b, -3*(c - a)),                                   # (가) 기울기 -3
       sp.Eq((c - b)**2 + (yC - a)**2, 50)]                          # 원 위
a0, c0 = solve_mn(m0, n0)[0]                                      # 수치해를 시작점으로
sol = sp.nsolve([e.lhs - e.rhs for e in eqs], (a, c),
                (sp.Float(str(a0)), sp.Float(str(c0))), prec=20)
av, cv = sol[0], sol[1]
bv = (2**(av - m0) + n0)
ratio = sp.Abs(av + bv)/(2*sp.Abs(cv - av))                          # (나) 넓이비
assert abs(sp.N(ratio) - sp.Rational(27, 8)) < 1e-6, '넓이비 재확인 실패'
print('VERIFY_PASS' if sp.Integer(best) == CANDIDATE else 'VERIFY_FAIL')
