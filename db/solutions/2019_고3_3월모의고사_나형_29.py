"""
2019년 고3 3월 모의고사 나형 29번 — 파라미터화 솔버.

[문제 구조]
자연수 m에 대해, a × b^m 이 "첫째항 a, 공비 r(자연수, r ≥ c)인 등비수열의 제k항"이
되도록 하는 모든 자연수 k의 값의 합을 A(m)이라 한다.

  a × b^m = a × r^{k-1}  ⟺  r^{k-1} = b^m

b = ∏ p_i^{e_i} 로 소인수분해하면, b^m = ∏ p_i^{e_i·m}.
r^{n} = b^m (n := k-1) 이 자연수 r을 가지려면 n 이 gcd(e_i·m) = m·g 를 나누어야 한다
(g := gcd(e_1,...,e_l), b의 소인수 지수들의 최대공약수). 이때
  r = ∏ p_i^{(e_i·m)/n}
로 r이 유일하게 정해지며, n(=k-1)이 작아질수록(=k가 작아질수록) r은 커진다.
"공비 r ≥ c" 조건을 만족하는 n만 남기면

  A(m) = Σ_{n | m·g, r(n) ≥ c} (n+1)

원문제는 a=3(첫째항, 항상 소거되어 답에 무관하므로 파라미터로 두지 않음),
b=2(소수), c=2(공비 하한 "2 이상"), m=200 인 경우이다.
이때 g=gcd(1)=1 이므로 n은 m의 약수 전체이고, r=2^{m/n} ≥ 2^1 = 2 = c 가 항상
성립해 모든 n|m 이 유효 → A(m)=Σ_{d|m}(d+1)=σ(m)+τ(m)=465+12=477.

[실제로 답을 바꾸는 파라미터]
- m : 대상 지수 (원문 m=200)
- b : 3×b^m 의 밑 (원문 b=2). b의 소인수 지수 구조(g)가 달라지면 유효한 k의
      집합·개수가 통째로 달라져 답이 바뀜.
- c : 공비 하한 (원문 "2 이상" → c=2). c를 올리면 r이 작은(=n이 큰, 즉 k가 작은)
      항들이 탈락하여 답이 줄어듦.
"""
import sympy as sp


def A(m, b, c):
    """조건을 만족하는 자연수 k의 값의 합 A(m) 을 실제로 계산한다."""
    factors = sp.factorint(b)          # b = ∏ p_i^{e_i}
    g = 0
    for e in factors.values():
        g = sp.gcd(g, e)               # g = gcd(e_1, ..., e_l)
    M = m * g

    total = 0
    for n in sp.divisors(M):           # n = k-1 후보
        r = 1
        for p, e in factors.items():
            r *= p ** ((e * m) // n)   # n | e*m 은 n|M=m*g, g|e 로부터 항상 보장됨
        if r >= c:                     # 공비 하한 조건
            total += (n + 1)           # k = n + 1
    return total


CANDIDATE = 477                        # ★ 원문제 정답 (절대 변경 금지)

PARAMS = dict(
    m=200,   # A(m) 의 m
    b=2,     # 3×b^m 의 밑
    c=2,     # 공비 하한 ("2 이상의 자연수")
)


def solve(prm):
    m, b, c = prm['m'], prm['b'], prm['c']
    if not (isinstance(m, int) and m >= 1):
        raise ValueError('m은 자연수여야 합니다.')
    if not (isinstance(b, int) and b >= 2):
        raise ValueError('b는 2 이상의 자연수여야 합니다.')
    if not (isinstance(c, int) and c >= 2):
        raise ValueError('c는 2 이상의 자연수여야 합니다.')
    return A(m, b, c)


def statement(prm):
    m, b, c = prm['m'], prm['b'], prm['c']
    return (
        "자연수 m에 대하여 다음 조건을 만족시키는 모든 자연수 k의 값의 합을 "
        "A(m)이라 하자.\n\n"
        f"  3 × {b}^m 은 첫째항이 3이고 공비가 {c} 이상의 자연수인 등비수열의 "
        "제k항이다.\n\n"
        f"A({m})의 값을 구하시오."
    )


# 문제 본문의 예시(m=2, b=2, c=2 → A(2)=5)로 구조 자체를 검증.
assert A(2, 2, 2) == 5, A(2, 2, 2)

# b, c가 실제로 답을 바꾸는 파라미터인지(장식이 아닌지) 직접 확인.
assert solve(dict(m=200, b=2, c=3)) != CANDIDATE
assert solve(dict(m=200, b=4, c=2)) != CANDIDATE

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
