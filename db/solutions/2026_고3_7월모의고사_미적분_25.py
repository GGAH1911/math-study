# 2026 고3 7월 미적분 25 — 파라미터화 솔버
#   조건:  lim (a_n + p·n^2)/(q·n^2 + r) = L      (모든 항이 양수인 수열 a_n)
#   구할값: lim k/(√(a_n + s·n) − √(a_n + t·n))
# 구조: 조건식이 a_n 의 최고차항 계수 c 를 결정하고(a_n ~ c·n^2),
#       그 c 만으로 목표 극한이 정해진다 → 하위항을 섞어도 값이 불변임을 코드가 확인한다.
import sympy as sp

CANDIDATE = 5

PARAMS = dict(
    p=1,                      # 조건식 분자의 n^2 계수  (a_n + p·n^2)
    q=2,                      # 조건식 분모의 n^2 계수  (q·n^2 + r)
    r=4,                      # 조건식 분모의 상수항
    L=2,                      # 조건식의 극한값
    k=1,                      # 구하는 식의 분자
    s=3,                      # √(a_n + s·n)
    t=1,                      # √(a_n + t·n)
    choices=[sp.sqrt(3)/9, sp.Rational(1, 3), sp.sqrt(3)/3, sp.Integer(1), sp.sqrt(3)],
)

n = sp.Symbol('n', positive=True)


def lead_coeff(prm):
    """조건 lim (a_n + p n^2)/(q n^2 + r) = L 에서 a_n 의 최고차항 계수 c 를 뽑는다."""
    c = sp.Symbol('c', positive=True)
    cond = sp.Eq(sp.limit((c*n**2 + prm['p']*n**2)/(prm['q']*n**2 + prm['r']), n, sp.oo), prm['L'])
    sols = [x for x in sp.solve(cond, c) if x.is_real and x.is_positive]
    return sols[0] if sols else None


def target_value(prm, c, tail=0):
    """a_n = c·n^2 + tail·n 을 실제로 대입해 목표 극한을 계산."""
    a = c*n**2 + tail*n
    return sp.simplify(sp.limit(prm['k']/(sp.sqrt(a + prm['s']*n) - sp.sqrt(a + prm['t']*n)), n, sp.oo))


def solve(prm=PARAMS):
    c = lead_coeff(prm)
    if c is None:                       # 조건을 만족하는 양수 수열이 없음
        return None
    val = target_value(prm, c)
    # 조건이 최고차항만 묶는데도 답이 정해지는지 확인 — 하위항(7n)을 섞어도 같은 값이어야 한다.
    if sp.simplify(val - target_value(prm, c, tail=7)) != 0:
        return None
    for i, ch in enumerate(prm['choices'], 1):
        if sp.simplify(val - sp.sympify(ch)) == 0:
            return i                    # 보기와 대조해 번호를 결정
    return val                          # 보기 밖(변형문제) → 값 자체를 답으로 돌려준다


def choice_set(prm):
    """주어진 보기에 답이 없으면(=변형문제) 답을 포함한 보기 세트를 새로 만든다."""
    val = target_value(prm, lead_coeff(prm))
    ch = list(prm['choices'])
    if all(sp.simplify(val - sp.sympify(x)) != 0 for x in ch):
        ch = [val/3, val/2, val, val*2, val*3]
    return ch


def variant(prm):
    """변형문제 한 벌: (문제 문장, 정답 보기번호). 보기 세트까지 맞춰 solve 로 번호를 확정한다."""
    p2 = {**prm, 'choices': choice_set(prm)}
    return statement(p2), solve(p2)


def statement(prm=PARAMS):
    ch = choice_set(prm)
    opts = ' '.join(f'{"①②③④⑤"[i]}{sp.latex(sp.sympify(v))}' for i, v in enumerate(ch))
    co = lambda x, sym='n': ('' if x == 1 else str(x)) + sym          # 계수 1 은 생략
    return (f"모든 항이 양수인 수열 {{a_n}} 에 대하여 "
            f"lim (a_n + {co(prm['p'], 'n^2')})/({co(prm['q'], 'n^2')} + {prm['r']}) = {prm['L']} 일 때, "
            f"lim {prm['k']}/(√(a_n + {co(prm['s'])}) − √(a_n + {co(prm['t'])})) 의 값은?\n  {opts}")


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
