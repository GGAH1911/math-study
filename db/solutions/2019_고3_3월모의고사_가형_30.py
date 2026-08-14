import sympy as sp
from collections import Counter

CANDIDATE = 77  # ★원문제 정답 (절대 변경 금지)

# 문제의 수학 구조를 이루는 파라미터
#   c : g(x) = c*x*e^(1-x) + k 에서 x의 계수 (원문제 3)
#   N : (나) 조건의 자연근 상한 "N 이하의 자연수" (원문제 10)
#   T : (다) 조건에서 요구하는 "자연수 k의 개수" (원문제 4)
PARAMS = dict(c=3, N=10, T=4)


def solve(prm):
    c, N, T = prm['c'], prm['N'], prm['T']

    # --- sympy로 g(x)=c*x*e^{1-x}+k 의 임계점과 극값을 실제로 계산 ---
    x, kk = sp.symbols('x k')
    g = c * x * sp.exp(1 - x) + kk
    gp = sp.diff(g, x)
    crit = sp.solve(sp.Eq(gp, 0), x)
    real_crit = [r for r in crit if r.is_real]
    if len(real_crit) != 1:
        raise ValueError("g(x)의 임계점이 유일하지 않습니다 (문제 구조가 깨짐)")
    x0 = real_crit[0]
    gmax_expr = sp.simplify(g.subs(x, x0))  # = c + k  (극댓값, x=1에서)

    # g는 x0에서 유일 극대이고 x0 왼쪽에서 -inf -> gmax, 오른쪽에서 gmax -> k(점근선)
    # 로 단조이므로, f의 단순근 r 에 대해 |f∘g| 가 미분가능하려면
    # r >= gmax(k) = c+k 이어야 함 (r가 gmax(k)보다 작으면 g'≠0인 두 지점에서 접촉).
    def threshold(kval):
        return int(gmax_expr.subs(kk, kval))

    def works(roots, kval):
        thr = threshold(kval)
        for r, m in roots.items():
            if m == 1 and r < thr:
                return False
        return True

    def f0(roots):
        # f(x) = prod (x-r)^m, 최고차항 계수 1 ; f(0) 을 sympy로 직접 전개해서 계산
        xs = sp.symbols('xs')
        expr = sp.Integer(1)
        for r, m in roots.items():
            expr *= (xs - r) ** m
        return int(sp.expand(expr).subs(xs, 0))

    valid = []
    seen = set()
    k_search_bound = N + T + c + 50  # 근이 N 이하이므로 이보다 큰 k는 무의미
    for a in range(1, N + 1):
        for b in range(a, N + 1):
            roots = Counter([1, 1, a, b])  # (x-1)^2 (x-a)(x-b), 최고차항 1
            key = tuple(sorted(roots.items()))
            if key in seen:
                continue
            seen.add(key)

            has_simple = any(m == 1 for m in roots.values())
            if not has_simple:
                continue  # 단순근이 없으면 조건이 항상 성립 -> k가 무한히 많아 (다) 불가능

            cnt = sum(1 for kv in range(1, k_search_bound) if works(roots, kv))
            if cnt == T:
                valid.append(f0(roots))

    if not valid:
        raise ValueError("주어진 (c, N, T) 조합을 만족하는 사차함수가 존재하지 않습니다")

    return max(valid) + min(valid)


def statement(prm):
    c, N, T = prm['c'], prm['N'], prm['T']
    return (
        "다음 조건을 만족시키며 최고차항의 계수가 1인 모든 사차함수 f(x)에 대하여 "
        "f(0)의 최댓값과 최솟값의 합을 구하시오. "
        "(단, lim_{x→∞} x/e^x = 0)\n"
        "(가) f(1)=0, f'(1)=0\n"
        f"(나) 방정식 f(x)=0의 모든 실근은 {N} 이하의 자연수이다.\n"
        f"(다) 함수 g(x)={c}x/e^(x-1)+k에 대하여 함수 |(f∘g)(x)|가 실수 전체의 집합에서 "
        f"미분가능하도록 하는 자연수 k의 개수는 {T}이다."
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
