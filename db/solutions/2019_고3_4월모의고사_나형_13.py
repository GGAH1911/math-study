"""2019 고3 4월모의고사 나형 13번 — 파라미터화 솔버.

문제 구조: 크기 3인 집합 X 위의 두 일대일대응(순열) f, g.
  - f 는 그림으로 주어진 순열(3개 원소의 순열 6가지 중 하나).
  - g 는 "모든 k 에 대해 f(k)\\neq g(k)"(f 와 자리마다 다름)와
    "g(a)=b"(특정 한 자리 값 지정) 두 조건을 만족.
  - 질문은 f^{-1}(qf) + g(qg).

수학적으로는: X 의 모든 순열(3!=6개) 중 g(a)=b 이고 모든 k 에서 f(k)\\neq g(k) 인
것을 sympy 없이도 되는 순수 조합론이지만, 여기서는 sympy 로 최종 값의 정수성/유일성을
검증한다. g(a)=b 로 한 자리가 고정되면 남은 두 자리를 채우는 방법은 2가지뿐이고,
"자리마다 다름" 조건이 그중 하나를 걸러내 g 가 유일하게 결정되는 구조 — 이 유일성이
무너지면(즉 g 가 여러 개거나 하나도 없으면) 문제로 성립하지 않으므로 예외를 던진다.

파라미터화(값을 실제로 바꾸는 손잡이, 5개):
  f_idx  : f 로 쓸 순열을 permutations(X) 중에서 고르는 인덱스 (mod 6)
  ga_idx : g(a)=b 조건의 정의역 값 a 를 X 에서 고르는 인덱스 (mod 3)
  gb_idx : g(a)=b 조건의 치역 값 b 를 X 에서 고르는 인덱스 (mod 3)
  qf_idx : f^{-1}(qf) 에서 물어보는 값 qf 를 X 에서 고르는 인덱스 (mod 3)
  qg_idx : g(qg) 에서 물어보는 값 qg 를 X 에서 고르는 인덱스 (mod 3)
모두 mod 연산으로 감싸 어떤 정수를 넣어도(perturbation +1/+2/*2 포함) 항상
X 안의 값으로 해석되므로, "존재하지 않는 원소" 때문에 죽는 대신 실제로 다른
문제 인스턴스가 만들어진다(단, g 가 유일하게 결정되지 않는 조합은 규칙대로 예외).
"""
import itertools

X = (2, 4, 6)                       # 원문제의 집합 X (레이블 자체는 구조가 아니라 표기이므로 고정)
PERMS = list(itertools.permutations(X))   # X 위의 모든 일대일대응(순열) 6개


def _decode(prm):
    n = len(X)
    f_tuple = PERMS[prm['f_idx'] % len(PERMS)]
    f = dict(zip(X, f_tuple))
    a = X[prm['ga_idx'] % n]
    b = X[prm['gb_idx'] % n]
    qf = X[prm['qf_idx'] % n]
    qg = X[prm['qg_idx'] % n]
    return f, a, b, qf, qg


def value(prm):
    """f^{-1}(qf) + g(qg) 를 실제로 계산한다(조건을 만족하는 g 를 전수 탐색으로 유일 결정)."""
    f, a, b, qf, qg = _decode(prm)
    finv = {v: k for k, v in f.items()}

    candidates = set()
    for gt in PERMS:                              # g: X 위의 일대일대응 전수 탐색
        g = dict(zip(X, gt))
        if g[a] != b:                              # 조건: g(a) = b
            continue
        if any(g[k] == f[k] for k in X):           # 조건: 모든 k 에 f(k) \neq g(k)
            continue
        candidates.add(g[qg])

    if len(candidates) != 1:
        # g 가 유일하게 결정되지 않으면(0개 또는 2개 이상) 이 파라미터 조합은
        # 원문제와 같은 "유일하게 답이 정해지는" 문제로 성립하지 않는다.
        raise ValueError(f"g(qg)가 유일하게 결정되지 않음: {candidates}")
    return finv[qf] + candidates.pop()


def choices(prm):
    """원문제의 보기 형태(공차 2인 등차수열, 정답이 두 번째 자리)를 값에서 유도."""
    v = value(prm)
    return tuple(v + 2 * (i - 1) for i in range(5))


def solve(prm):
    """이 문제의 정답은 '보기 번호'가 아니라 '식의 값'으로 채점된다(원문제 CANDIDATE=값)."""
    return value(prm)


def statement(prm):
    f, a, b, qf, qg = _decode(prm)
    f_desc = ',\\ '.join(f"{k}\\to{f[k]}" for k in X)
    return (
        f"집합 X = \\{{{X[0]}, {X[1]}, {X[2]}\\}}에 대하여 X에서 X로의 일대일대응인 두 함수 f, g가 있다. "
        f"함수 f는 그림에서 ${f_desc}$로 대응된다.\n"
        f"집합 X의 모든 원소 k에 대하여 f(k) \\neq g(k)이고 g({a})={b}일 때, "
        f"f^{{-1}}({qf})+g({qg})의 값은?"
    )


CANDIDATE = 6   # ★원문제 정답 (보기 ② 의 값) — 절대 바꾸지 않음

PARAMS = dict(
    f_idx=3,    # permutations(X)[3] = (4,6,2) → f(2)=4, f(4)=6, f(6)=2 (그림의 3-순환)
    ga_idx=0,   # a = X[0] = 2  → g(2) = ...
    gb_idx=2,   # b = X[2] = 6  → g(2) = 6
    qf_idx=2,   # qf = X[2] = 6 → f^{-1}(6)
    qg_idx=1,   # qg = X[1] = 4 → g(4)
)

# 원문제 보기 ①4 ②6 ③8 ④10 ⑤12 가 그대로 유도되는지 고정 검증
assert choices(PARAMS) == (4, 6, 8, 10, 12)
assert solve(PARAMS) == CANDIDATE

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
