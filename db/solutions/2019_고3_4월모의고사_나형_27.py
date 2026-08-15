import sympy as sp
from sympy import log, symbols

CANDIDATE = 36  # ★원문제 정답 — 절대 바꾸지 않음

# 문제 구조:
#   세 실수 t, a, b 가 이 순서대로 등비수열을 이룬다 → a = t*q, b = t*q^2 (공비 q)
#   조건식: log_a(t*b) + log_t(b) = k
#   원문제는 t=3(등비수열 첫째항이자 log_a(3b)의 "3"), k=5.
#   log_a(t*b)식 안의 계수가 등비수열의 첫째항 t와 "같은 3"이라는 점이 원문제의
#   구조적 핵심이다(그래서 t*b = t^2*q^2 = a^2 이 되어 log_a(t*b)=2 로 깔끔히 정리됨).
#   이 결합을 유지한 채 t(첫째항), k(로그식 우변 상수) 두 값을 파라미터로 뽑는다.
PARAMS = dict(t=3, k=5)


def solve(prm):
    """등비수열 + 로그방정식 조건에서 a+b 를 sympy 로 실제로 구한다."""
    t = sp.nsimplify(prm['t'])
    k = sp.nsimplify(prm['k'])
    if t <= 0 or t == 1:
        raise ValueError('등비수열 첫째항 t 는 1이 아닌 양수여야 합니다.')

    q = symbols('q', positive=True, real=True)
    a = t * q
    b = t * q**2

    # log_a(t*b) + log_t(b) = k
    equation = log(t * b, a) + log(b, t) - k
    sols = sp.solve(equation, q)
    sols = [s for s in sols if s.is_real and s.is_positive]
    if not sols:
        raise ValueError(f'주어진 t={t}, k={k} 에서 조건을 만족하는 공비 q 가 없습니다.')

    q_val = sols[0]
    a_val = t * q_val
    b_val = t * q_val**2

    # 검증: 원래 로그식이 k 를 만족하는지 재확인 (a, b 가 1이 되면 밑 조건 위배)
    if a_val == 1 or b_val <= 0:
        raise ValueError('a 또는 b 가 로그의 밑/진수 조건을 위배합니다.')
    check = sp.simplify(log(t * b_val, a_val) + log(b_val, t) - k)
    if sp.simplify(check) != 0:
        raise ValueError('조건식을 만족하지 않는 해입니다.')

    return sp.nsimplify(a_val + b_val)


def statement(prm):
    t, k = prm['t'], prm['k']
    return (
        f"세 실수 {t}, a, b가 이 순서대로 등비수열을 이루고 "
        f"log_a({t}b) + log_{t} b = {k}를 만족시킨다. a+b의 값을 구하시오."
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
