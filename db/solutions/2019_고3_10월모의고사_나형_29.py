"""
2019 고3 10월모의고사 나형 29번 — 파라미터화 솔버

수열 {a_n}: 첫째항이 짝수이고, 모든 자연수 n에 대해
  a_n이 홀수이면 a_(n+1) = a_n + c
  a_n이 짝수이면 a_(n+1) = a_n / 2
를 만족한다. a_N = target 일 때, 수열의 첫째항이 될 수 있는 모든 수의 합을 구한다.

원문제: c=3, N=5, target=5, 첫째항은 짝수 → 답 142
  역추적: 5←10←{20,7}←{40,17,14}←{80,34,28}(짝수만) → 80+34+28=142

파라미터로 뽑아낸 수학 구조
  - c        : 홀수 분기에서 더하는 상수 (a_n → a_n + c)
  - target   : 마지막에 주어진 값 a_N
  - steps    : N-1, 즉 a_N에서 a_1까지 거슬러 올라가는 횟수 (N = steps+1)
  - first_parity : 첫째항이 만족해야 하는 나머지 조건 (0=짝수, 1=홀수)

역추적(전이의 역함수)을 각 단계마다 sympy로 실제 방정식을 세워 푼다.
  - 직전 항이 짝수 분기였다면: a/2 = v  →  a = 2v  (자연수이면 항상 유효, 짝수)
  - 직전 항이 홀수 분기였다면: a + c = v  →  a = v - c  (a가 자연수이면서 홀수일 때만 유효)
"""
import sympy as sp

CANDIDATE = 142

PARAMS = dict(c=3, target=5, steps=4, first_parity=0)


def preimages(v, c):
    """값 v(=a_(k+1))를 만들어낼 수 있는 직전 항 a_k 후보들을 sympy로 구한다."""
    a = sp.symbols('a')
    res = []

    # 짝수 분기였을 경우: a/2 = v
    for s in sp.solve(sp.Eq(a / 2, v), a):
        s = sp.nsimplify(s)
        if s.is_integer and s > 0:
            res.append(int(s))

    # 홀수 분기였을 경우: a + c = v, 단 a는 홀수인 자연수
    for s in sp.solve(sp.Eq(a + c, v), a):
        s = sp.nsimplify(s)
        if s.is_integer and s > 0 and int(s) % 2 == 1:
            res.append(int(s))

    return res


def solve(prm):
    c = prm['c']
    layer = {prm['target']}
    for _ in range(prm['steps']):
        nxt = set()
        for v in layer:
            for p in preimages(v, c):
                nxt.add(p)
        layer = nxt
        if not layer:
            raise ValueError("역추적 중 후보가 사라졌습니다 (해가 존재하지 않는 파라미터 조합)")

    candidates = [a for a in layer if a % 2 == prm['first_parity']]
    if not candidates:
        raise ValueError("조건을 만족하는 첫째항 후보가 없습니다")
    return sum(candidates)


def statement(prm):
    parity_word = '짝수' if prm['first_parity'] == 0 else '홀수'
    n_last = prm['steps'] + 1
    return (
        f"첫째항이 {parity_word}인 수열 {{a_n}}은 모든 자연수 n에 대하여 "
        f"a_(n+1) = a_n + {prm['c']} (a_n이 홀수인 경우), "
        f"a_(n+1) = a_n / 2 (a_n이 짝수인 경우)를 만족시킨다. "
        f"a_{n_last} = {prm['target']}일 때, 수열 {{a_n}}의 첫째항이 될 수 있는 "
        f"모든 수의 합을 구하시오."
    )


if __name__ == '__main__':
    print(statement(PARAMS))
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
