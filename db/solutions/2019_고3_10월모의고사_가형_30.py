import sympy as sp

CANDIDATE = 26  # ★원문제 정답, 절대 변경 금지

# ------------------------------------------------------------------
# 문제의 수학 구조
#   (가) g(x+1) - g(x) = -k*pi*(e+1)*e^x*sin(pi*x)
#        -> g(x) = C*e^x*sin(pi*x), C = k*pi 로 유일하게 결정됨
#   (나) g(x+1) = ∫_0^x { f(t+1)e^t - f(t)e^t + g(t) } dt
#        -> 양변 미분: f(x+1)-f(x) = -k*pi*(e+1)*sin(pi*x) - k*pi^2*e*cos(pi*x)
#        -> 특수해 f_p(x)=P sin(pi x)+Q cos(pi x) (미정계수법으로 sympy가 직접 계산)
#        -> f(x) = phi(x) + f_p(x), phi 는 주기 1 인 주기함수
#   ∫_0^1 f(x)dx = A*e + B  (주어진 조건)  →  ∫_0^1 phi dx = (A-k)e + (B-k)
#   ∫_1^n f(x)dx = (n-1)*∫_0^1 phi dx + ∫_1^n f_p dx
#
# 파라미터로 뽑아낸 것:
#   k : (가)의 우변 배율 (원문제 k=1) — g, f_p 를 모두 스케일시켜 답을 바꿈
#   A, B : ∫_0^1 f(x)dx = A*e + B 의 계수 (원문제 A=10/9, B=4) — phi의 크기를 직접 바꿔 답을 바꿈
#   n : 최종 적분 상한 ∫_1^n f(x)dx (원문제 n=10) — 주기 개수와 f_p 적분구간을 바꿔 답을 바꿈
# ------------------------------------------------------------------

PARAMS = dict(k=1, A=sp.Rational(10, 9), B=4, n=10)


def solve(prm):
    k = sp.nsimplify(prm['k'])
    A = sp.nsimplify(prm['A'])
    B = sp.nsimplify(prm['B'])
    n = prm['n']

    if not (isinstance(n, int) and n >= 2):
        raise ValueError("n 은 2 이상의 정수여야 합니다 (구간 [1,n] 이 성립해야 함).")
    if k == 0:
        raise ValueError("k=0 이면 g가 항등적으로 0이 되어 문제가 성립하지 않습니다.")

    x = sp.Symbol('x', real=True)
    e = sp.E
    pi = sp.pi

    # (가): g(x)=C*e^x*sin(pi*x) 형태로 두고 조건을 만족하는 C 를 sympy로 직접 결정
    C = sp.Symbol('C')
    g_trial = C * sp.exp(x) * sp.sin(pi * x)
    ga_lhs = sp.expand_trig(g_trial.subs(x, x + 1)) - g_trial
    ga_rhs = -k * pi * (e + 1) * sp.exp(x) * sp.sin(pi * x)
    # sin(pi x), cos(pi x) 계수를 비교하기 위해 두 점에서 방정식을 세워 C 를 구함
    eqC1 = sp.expand(ga_lhs - ga_rhs).subs(x, 0)
    eqC2 = sp.expand(ga_lhs - ga_rhs).subs(x, sp.Rational(1, 2))
    C_val = sp.solve([eqC1, eqC2], [C])[C]
    g = g_trial.subs(C, C_val)

    # 검증: (가)가 항등적으로 성립하는지
    check_ga = sp.simplify(sp.expand_trig(g.subs(x, x + 1)) - g - ga_rhs)
    if check_ga != 0:
        raise ValueError("조건 (가)를 만족하는 g를 구하지 못했습니다.")

    # (나)를 미분하여 얻는 함수방정식: f(x+1)e^x - f(x)e^x = g'(x+1) - g(x)
    gp = sp.diff(g, x)
    rhs_fe = sp.simplify((gp.subs(x, x + 1) - g) / sp.exp(x))
    # rhs_fe = -k*pi*(e+1)*sin(pi x) - k*pi^2*e*cos(pi x) 형태여야 함 -> 특수해를 미정계수법으로 구함
    P, Q = sp.symbols('P Q')
    f_p_expr = P * sp.sin(pi * x) + Q * sp.cos(pi * x)
    diff_expr = sp.expand(sp.expand_trig(f_p_expr.subs(x, x + 1)) - f_p_expr - rhs_fe)
    eq1 = diff_expr.subs(x, 0)
    eq2 = diff_expr.subs(x, sp.Rational(1, 2))
    sol = sp.solve([eq1, eq2], [P, Q])
    f_p = f_p_expr.subs(sol)

    # 검증: f_p 가 함수방정식을 만족하는지
    check_fp = sp.simplify(sp.expand_trig(f_p.subs(x, x + 1)) - f_p - rhs_fe)
    if check_fp != 0:
        raise ValueError("특수해 f_p 를 구하지 못했습니다.")

    int_fp_01 = sp.simplify(sp.integrate(f_p, (x, 0, 1)))

    # f(x) = phi(x) + f_p(x), phi 는 주기 1 인 주기함수
    # 주어진 조건 ∫_0^1 f dx = A*e+B 로부터 ∫_0^1 phi dx 를 결정
    int_phi_01 = sp.simplify(A * e + B - int_fp_01)

    # phi 는 주기 1 이므로 ∫_1^n phi dx = (n-1) * ∫_0^1 phi dx
    int_phi_1n = (n - 1) * int_phi_01

    int_fp_1n = sp.simplify(sp.integrate(f_p, (x, 1, n)))

    answer = sp.simplify(int_phi_1n + int_fp_1n)

    if not answer.is_number:
        raise ValueError("답이 수치로 확정되지 않았습니다.")

    answer = sp.nsimplify(answer)
    if answer == sp.floor(answer):
        answer = int(answer)
    return answer


def statement(prm):
    k = prm['k']
    A = prm['A']
    B = prm['B']
    n = prm['n']

    coef_txt = "" if k == 1 else (f"{k}" if k != -1 else "-")
    if k == -1:
        coef_txt = "-"

    A_txt = sp.latex(sp.nsimplify(A))

    return (
        "실수 전체의 집합에서 미분가능한 두 함수 f(x), g(x)가 모든 실수 x에 대하여 "
        "다음 조건을 만족시킨다.\n"
        "(가) g(x+1)-g(x)=-" + coef_txt + r"\pi(e+1)e^x\sin(\pi x)" + "\n"
        r"(나) g(x+1)=\int_0^x \{f(t+1)e^t-f(t)e^t+g(t)\}dt" + "\n"
        f"\\int_0^1 f(x)dx={A_txt}e+{B}일 때, "
        f"\\int_1^{{{n}}} f(x)dx의 값을 구하시오."
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
