"""2026 고3 7월 모의고사 공통 6번 — 로그 조건식 연립 (파라미터화 솔버).

원문제: 1보다 큰 두 실수 a, b 가
        log_{√a} b = 6,   log_4 a + log_2 b = 14
        를 만족시킬 때, log_2 (b/a) 의 값은?  [보기 6,7,8,9,10]

구조: x = log_2 a, y = log_2 b 로 치환하면 두 조건이 x, y 의 1차 연립방정식이 된다.
      ① log_{a^(1/r)} b = c1  ->  r·y = c1·x
      ② ca·log_{base_a} a + cb·log_{base_b} b = c2  ->  ca·x/log_2(base_a) + cb·y/log_2(base_b) = c2
      목표 log_{tb}(b^se / a^te) = (se·y - te·x)/log_2(tb).
      객관식이므로 구한 값을 보기와 대조해 보기 번호를 답으로 낸다.
"""
import sympy as sp

CANDIDATE = 3

PARAMS = dict(
    root_index=2,     # 첫 조건의 로그 밑 a^(1/root_index) — 원문제는 √a
    c1=6,             # 첫 조건의 값: log_{√a} b = 6
    coef_a=1,         # 둘째 조건에서 log_{base_a} a 의 계수
    base_a=4,         # 둘째 조건에서 a 쪽 로그의 밑
    coef_b=1,         # 둘째 조건에서 log_{base_b} b 의 계수
    base_b=2,         # 둘째 조건에서 b 쪽 로그의 밑
    c2=14,            # 둘째 조건의 값: log_4 a + log_2 b = 14
    target_base=2,    # 구하는 로그의 밑: log_2 (b/a)
    exp_b=1,          # 구하는 로그 진수의 b 지수 (b^exp_b)
    exp_a=1,          # 구하는 로그 진수의 a 지수 (a^exp_a)
    choices=(6, 7, 8, 9, 10),   # ①~⑤ 보기 값 (정답 번호는 solve 가 대조해 정한다)
)


def solve_value(prm):
    """두 로그 조건을 연립해 log_{target_base}(b^exp_b / a^exp_a) 의 값을 구한다."""
    x, y = sp.symbols('x y', real=True)        # x = log_2 a, y = log_2 b
    r = sp.nsimplify(prm['root_index'])
    la = sp.log(sp.nsimplify(prm['base_a']), 2)
    lb = sp.log(sp.nsimplify(prm['base_b']), 2)
    lt = sp.log(sp.nsimplify(prm['target_base']), 2)

    # ① log_{a^(1/r)} b = c1  ->  y / (x/r) = c1
    eq1 = sp.Eq(r * y, sp.nsimplify(prm['c1']) * x)
    # ② coef_a·log_{base_a} a + coef_b·log_{base_b} b = c2
    eq2 = sp.Eq(sp.nsimplify(prm['coef_a']) * x / la
                + sp.nsimplify(prm['coef_b']) * y / lb,
                sp.nsimplify(prm['c2']))

    sol = sp.solve([eq1, eq2], [x, y], dict=True)
    if not sol:
        raise ValueError('연립방정식이 유일하게 풀리지 않는다')
    xv = sp.simplify(sol[0][x])
    yv = sp.simplify(sol[0][y])

    # a > 1, b > 1  <=>  log_2 a > 0, log_2 b > 0
    if not (sp.simplify(xv).is_positive and sp.simplify(yv).is_positive):
        raise ValueError('a>1, b>1 조건을 만족하지 않는다')

    # 원 조건 재확인 (치환이 옳았는지 로그 식 그대로 검산)
    a, b = sp.Integer(2) ** xv, sp.Integer(2) ** yv
    chk1 = sp.simplify(sp.log(b, 2) / sp.log(a ** (sp.Integer(1) / r), 2) - sp.nsimplify(prm['c1']))
    chk2 = sp.simplify(sp.nsimplify(prm['coef_a']) * sp.log(a, 2) / la
                       + sp.nsimplify(prm['coef_b']) * sp.log(b, 2) / lb
                       - sp.nsimplify(prm['c2']))
    if sp.simplify(chk1) != 0 or sp.simplify(chk2) != 0:
        raise ValueError('원 조건 재검산 실패')

    return sp.simplify((sp.nsimplify(prm['exp_b']) * yv
                        - sp.nsimplify(prm['exp_a']) * xv) / lt)


def solve(prm):
    """객관식 답 — 구한 값이 보기에 있으면 그 보기 번호를, 없으면 값 자체를 돌려준다."""
    val = solve_value(prm)
    for i, c in enumerate(prm.get('choices') or [], start=1):
        if sp.simplify(val - sp.nsimplify(c)) == 0:
            return i
    return val


def statement(prm):
    """새 문제 문장(보기 포함)."""
    r = prm['root_index']
    base1 = '\\sqrt{a}' if r == 2 else f'a^{{1/{r}}}'
    ta = f"\\log_{{{prm['base_a']}}}a"
    tb = f"\\log_{{{prm['base_b']}}}b"
    if prm['coef_a'] != 1:
        ta = f"{prm['coef_a']}{ta}"
    if prm['coef_b'] != 1:
        tb = f"{prm['coef_b']}{tb}"
    num = 'b' if prm['exp_b'] == 1 else f"b^{{{prm['exp_b']}}}"
    den = 'a' if prm['exp_a'] == 1 else f"a^{{{prm['exp_a']}}}"
    body = (f"1보다 큰 두 실수 a, b가 \\log_{{{base1}}}b={prm['c1']}, "
            f"{ta}+{tb}={prm['c2']} 를 만족시킬 때, "
            f"\\log_{{{prm['target_base']}}}\\frac{{{num}}}{{{den}}}의 값은?")
    marks = '①②③④⑤'
    opts = ' '.join(f'{marks[i]} {sp.latex(sp.nsimplify(c))}'
                    for i, c in enumerate(prm.get('choices') or []))
    return f'{body}\n{opts}'


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
