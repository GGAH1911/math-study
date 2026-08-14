# 다항식 (coef·x + const)^power 의 전개식에서 x^deg1 의 계수 a, x^deg2 의 계수 b → a+b 는?
# 수학 구조: 이항정리. (px+q)^n 의 일반항 C(n,k) (px)^k q^(n-k) → x^k 의 계수 = C(n,k) p^k q^(n-k)
import sympy as sp

CANDIDATE = 4                      # 정답 = 보기 ④ (360)

PARAMS = dict(
    coef=3,                        # (coef*x + const)^power 의 x 계수
    const=1,                       # 상수항
    power=5,                       # 지수
    deg1=2,                        # a 로 읽는 차수
    deg2=3,                        # b 로 읽는 차수
    choices=[315, 330, 345, 360, 375],   # 보기 ①~⑤ (정답 번호는 solve 가 대조해서 정한다)
)


def term_coeff(prm, k):
    """(coef*x+const)^power 전개식에서 x^k 의 계수 — 이항정리."""
    n = sp.Integer(prm['power'])
    k = sp.Integer(k)
    if k < 0 or k > n:
        return sp.Integer(0)
    return sp.binomial(n, k) * sp.Integer(prm['coef'])**k * sp.Integer(prm['const'])**(n - k)


def value(prm):
    """a + b 의 값."""
    a = term_coeff(prm, prm['deg1'])
    b = term_coeff(prm, prm['deg2'])
    return sp.Integer(a + b)


def solve(prm):
    """조건 → 정답 보기 번호(1~5). 보기에 값이 없으면 0."""
    val = value(prm)
    for i, c in enumerate(prm['choices'], 1):
        if sp.simplify(val - sp.nsimplify(c)) == 0:
            return i
    return 0


def statement(prm):
    """새 문제 문장."""
    def lin(p, q):
        head = 'x' if p == 1 else ('-x' if p == -1 else f'{p}x')
        if q == 0:
            return head
        return f'{head}{"+" if q > 0 else "-"}{abs(q)}'
    body = (f"다항식 ({lin(prm['coef'], prm['const'])})^{{{prm['power']}}}의 전개식에서 "
            f"x^{{{prm['deg1']}}}의 계수를 a, x^{{{prm['deg2']}}}의 계수를 b라 할 때, "
            f"a+b의 값은?")
    opts = ' '.join(f'{n} {c}' for n, c in zip('①②③④⑤', prm['choices']))
    return f'{body}\n{opts}'


# 독립 검산: sympy 전개식에서 직접 계수를 뽑아 이항정리 결과와 대조
_x = sp.symbols('x')
_p = sp.Poly(sp.expand((PARAMS['coef'] * _x + PARAMS['const'])**PARAMS['power']), _x)
_chk = sp.Integer(_p.coeff_monomial(_x**PARAMS['deg1']) + _p.coeff_monomial(_x**PARAMS['deg2']))

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE and _chk == value(PARAMS) else 'VERIFY_FAIL')
