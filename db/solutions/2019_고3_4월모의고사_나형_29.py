"""2019 고3 4월모의고사 나형 29번 — 파라미터 솔버.

원문제: 자연수 a, b, c 가 (가) 모두 짝수이다 (나) a×b×c = 10^5 일 때,
       순서쌍 (a, b, c) 의 개수를 구하시오. (답 126)

수학 구조
  N = a×b×c 를 소인수분해하면 N = p_even^e_even × p_other^e_other (서로 다른 두 소수).
  변수는 n개(a,b,c,...)이고, 그중 "짝수 조건"은 특정 소수 p_even 로 나누어떨어져야
  한다는 뜻 — 즉 각 변수의 p_even 지수 x_i ≥ 1.
    Σ x_i = e_even, x_i ≥ 1 (n개)  →  별-막대: C(e_even-1, n-1)
    다른 소수 p_other 는 조건이 없어 y_i ≥ 0                →  C(e_other+n-1, n-1)
  전체 경우의 수 = 두 값의 곱 (독립 분배이므로).

파라미터로 뽑아낸 것: p_even/p_other(어느 소수인지 — 값 자체는 답에 영향 없음,
문장 생성용), e_even/e_other(각 소수의 지수 — 답을 바꾸는 핵심 변수),
n(변수 개수, 즉 a,b,c 가 몇 개인지 — 답을 바꾸는 핵심 변수).

원문제: p_even=2, p_other=5, e_even=5, e_other=5, n=3
  → C(5-1,3-1)=C(4,2)=6, C(5+3-1,3-1)=C(7,2)=21, 6×21=126.
"""
import sympy as sp
from math import comb


PARAMS = dict(
    p_even=2,      # "짝수(=이 소수의 배수)" 조건이 걸리는 소수
    p_other=5,     # 조건 없는 다른 소수
    e_even=5,      # N 에서 p_even 의 지수
    e_other=5,     # N 에서 p_other 의 지수
    n=3,           # 변수 개수 (a, b, c, ... 몇 개인지)
)


def solve(prm):
    """조건 → 답.

    N = p_even^e_even * p_other^e_other 를 실제로 sympy.factorint 로 분해한 뒤,
    각 소수별 지수를 n개의 변수에 별-막대(stars and bars)로 분배하는 경우의 수를 곱한다.
    p_even 지수는 각 변수 몫이 ≥1 이어야 하므로(짝수 조건) C(e-1, n-1),
    그 외 소수는 ≥0 이어도 되므로 C(e+n-1, n-1).
    """
    p_even, p_other = prm['p_even'], prm['p_other']
    e_even, e_other, n = prm['e_even'], prm['e_other'], prm['n']

    if not (sp.isprime(p_even) and sp.isprime(p_other)):
        raise ValueError('p_even, p_other 는 소수여야 한다')
    if p_even == p_other:
        raise ValueError('p_even 과 p_other 는 서로 달라야 한다')
    if n < 1 or e_even < 0 or e_other < 0:
        raise ValueError('n≥1, 지수≥0 이어야 한다')

    N = p_even ** e_even * p_other ** e_other
    f = sp.factorint(N)   # 실제로 소인수분해를 수행

    total = 1
    for p, e in f.items():
        if p == p_even:
            if e < n:
                return 0            # 변수 n개 모두 p_even 배수이려면 지수가 n개 이상 필요
            total *= comb(e - 1, n - 1)
        else:
            total *= comb(e + n - 1, n - 1)
    return total


def statement(prm):
    p_even, p_other = prm['p_even'], prm['p_other']
    e_even, e_other, n = prm['e_even'], prm['e_other'], prm['n']
    names = ['a', 'b', 'c', 'd', 'e', 'f', 'g'][:n]
    var_list = ', '.join(names)
    N = p_even ** e_even * p_other ** e_other
    cond_even = '모두 짝수이다' if p_even == 2 else f'모두 {p_even}의 배수이다'
    return (
        f"다음 조건을 만족시키는 자연수 {var_list}의 모든 순서쌍 ({var_list})의 "
        f"개수를 구하시오.\n"
        f"(가) {var_list}는 {cond_even}.\n"
        f"(나) {' × '.join(names)} = {N} (= {p_even}^{e_even} × {p_other}^{e_other})"
    )


CANDIDATE = 126
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
