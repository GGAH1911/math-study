# 등비수열 a_n=a r^{n-1} (급수 수렴 → |r|<1). b_n 은 조건부 정의:
#   a_n ≤ a_{n+1} 이면 b_n=-a_n,  a_n > a_{n+1} 이면 b_n=a_{M·n}   (원문제 M=2)
# 조건 (가) a_n·b_n<0 → a>0, -1<r<0 이 강제되고, 그때 n 홀수면 b_n=a_{Mn}, 짝수면 b_n=-a_n.
# 조건 (나) (Σ|a_n|)^2 = C·Σ a_n^2 → (1-r)=C(1+r) → r=(1-C)/(1+C) 로 공비가 결정된다.
# 조건 (다) Σ(a_n+b_n)=S 로 첫항 a 가 결정되고, 마지막으로 Σ b_{J·n} 을 구한다.
# 파라미터화: C(제곱합 계수)·S(총합)·M(조건부 정의의 첨자 배수)·J(구하는 부분수열 간격).
# 유사문제 생성 시 유효범위: C>1 (그래야 -1<r<0), M 은 짝수 (홀수면 (가) a_n b_n<0 이 깨진다), J≥1.
CANDIDATE = 30
import sympy as sp

PARAMS = dict(sq_coeff=2, total=63, sub_index=2, target_step=2)


def solve(prm):
    C = sp.Rational(prm['sq_coeff'])          # (나) 우변 계수
    S = sp.Rational(prm['total'])             # Σ(a_n+b_n)
    M = int(prm['sub_index'])                 # b_n = a_{M n} (a_n > a_{n+1} 인 경우)
    J = int(prm['target_step'])               # 구하는 값 Σ b_{J n}

    a = sp.symbols('a', positive=True)
    r = sp.symbols('r', real=True)

    # ── (나) 로 공비 r 결정: Σ|a_n| = a/(1+r) (|r|=-r), Σa_n^2 = a^2/(1-r^2)
    eq = sp.Eq((1 / (1 + r))**2, C / (1 - r**2))
    cands = [s for s in sp.solve(eq, r) if s.is_real and -1 < s < 0]
    if not cands:
        raise ValueError('조건 (나) 를 만족하는 -1<r<0 이 없다')
    r0 = sp.nsimplify(cands[0])

    n = sp.symbols('n', positive=True, integer=True)
    b_odd = lambda k: a * r0**(M * k - 1)     # k 가 홀수인 자리: b_k = a_{Mk}
    b_even = lambda k: -a * r0**(k - 1)       # k 가 짝수인 자리: b_k = -a_k

    def Sb(step):
        """Σ_{n≥1} b_{step·n}. step 이 짝수면 첨자가 항상 짝수, 홀수면 n 의 홀짝을 따라간다."""
        if step % 2 == 0:
            return sp.summation(b_even(step * n), (n, 1, sp.oo))
        return (sp.summation(b_odd(step * (2 * n - 1)), (n, 1, sp.oo))
                + sp.summation(b_even(2 * step * n), (n, 1, sp.oo)))

    # ── (다) 로 첫항 a 결정 후 목표값 계산
    Sa = a / (1 - r0)
    a0 = sp.solve(sp.Eq(sp.simplify(Sa + Sb(1)), S), a)[0]
    return sp.nsimplify(sp.simplify(Sb(J).subs(a, a0)))


def statement(prm):
    C, S, M, J = prm['sq_coeff'], prm['total'], prm['sub_index'], prm['target_step']
    return (f"등비수열 {{a_n}} 에 대하여 급수 Σa_n 이 수렴하고, 수열 {{b_n}} 을 모든 자연수 n 에 대하여\n"
            f"  b_n = -a_n            (a_n ≤ a_{{n+1}} 일 때)\n"
            f"  b_n = a_{{{M}n}}          (a_n > a_{{n+1}} 일 때)\n"
            f"라 할 때, 두 수열 {{a_n}}, {{b_n}} 은 다음 조건을 만족시킨다.\n"
            f"  (가) 모든 자연수 n 에 대하여 a_n·b_n < 0 이다.\n"
            f"  (나) (Σ|a_n|)^2 = {C}·Σ(a_n)^2\n"
            f"Σ(a_n + b_n) = {S} 일 때, Σ b_{{{J}n}} 의 값을 구하시오.")


print('VERIFY_PASS' if sp.simplify(solve(PARAMS) - CANDIDATE) == 0 else 'VERIFY_FAIL')
