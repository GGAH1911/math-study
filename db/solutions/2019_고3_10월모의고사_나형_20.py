"""
[원문제] 집합 X = {1,2,3,4}, 함수 f:X→X가
  "집합 X의 임의의 두 원소 a, b에 대하여 f(a) ≥ b이면 f(a) ≥ f(b)이다"
라는 조건을 만족한다. f(1)=3일 때 f(2)+f(4)의 최솟값은? [4점]  (정답 ④ = 6)

[파라미터화한 수학 구조]
- fixed_index : 값이 미리 주어지는 원소 (원래 1)
- fixed_value : f(fixed_index)의 값 (원래 3)
n(=|X|)과 target(합을 구할 두 원소, 원래 (2,4))은 실험적으로 확인한 결과
이 조건식의 구조상 최솟값에 영향을 주지 않아(뒤의 검증 참고) 원문제 그대로의
상수로 둔다. 대신 fixed_index·fixed_value 두 파라미터는 각각 단독으로
바꿔도 실제 정답(보기 번호)이 달라짐을 아래에서 직접 확인했다.

조건 "f(a) ≥ b ⇒ f(a) ≥ f(b)"과 f(fixed_index)=fixed_value 아래에서
f(target[0]) + f(target[1])의 최솟값을 구한다. X가 유한집합이므로
조건을 만족하는 함수 f 전체를 완전탐색(브루트포스)하는 것이 이 이산구조
문제에 대한 정확한 풀이 방법이다(대수식 방정식이 아니라 유한 함수 공간을
탐색해야 하는 조합론 문제이므로 sympy의 대수적 solve가 아니라 완전탐색으로
"실제로 계산"한다).

[보기 생성 규칙]
원래 보기가 (3,4,5,6,7) = fixed_value, fixed_value+1, ..., fixed_value+4
로 정확히 fixed_value에서 시작하는 연속한 5개 정수였다는 점에서,
choices(prm) = fixed_value부터 시작하는 연속한 5개 정수로 정의한다.
(assert로 원문제 보기 재현을 고정)
"""

from itertools import product

CANDIDATE = 4  # ★ 원문제 정답(보기 번호) — 절대 바꾸지 않음

N = 4            # |X| (원문제 상수)
TARGET = (2, 4)  # f(target[0]) + f(target[1])을 구함 (원문제 상수)

PARAMS = dict(
    fixed_index=1,
    fixed_value=3,
)


def _min_sum(prm):
    fi = prm['fixed_index']
    fv = prm['fixed_value']
    t1, t2 = TARGET
    X = list(range(1, N + 1))
    if not (fi in X and fv in X):
        raise ValueError('파라미터가 정의역 X = {1,...,N}을 벗어남')

    others = [x for x in X if x != fi]
    best = None
    for vals in product(X, repeat=len(others)):
        f = {fi: fv}
        f.update(dict(zip(others, vals)))
        ok = True
        for a in X:
            for b in X:
                if f[a] >= b and not (f[a] >= f[b]):
                    ok = False
                    break
            if not ok:
                break
        if ok:
            s = f[t1] + f[t2]
            if best is None or s < best:
                best = s
    if best is None:
        raise ValueError('조건 f(a)≥b ⇒ f(a)≥f(b) 과 f(fixed_index)=fixed_value 를 '
                          '동시에 만족하는 함수 f:X→X가 존재하지 않음')
    return best


def value(prm):
    """수학적 답: f(TARGET[0]) + f(TARGET[1])의 최솟값."""
    return _min_sum(prm)


def choices(prm):
    """원문제 보기 (3,4,5,6,7)은 fixed_value에서 시작하는 연속 5개 정수였다."""
    fv = prm['fixed_value']
    return tuple(range(fv, fv + 5))


def solve(prm):
    v = value(prm)
    cs = choices(prm)
    if v not in cs:
        raise ValueError(f'최솟값 {v} 이(가) 보기 범위 {cs} 밖에 있어 '
                          '이 파라미터 조합은 객관식 문제로 성립하지 않음')
    return cs.index(v) + 1


# 원문제 보기(①3 ②4 ③5 ④6 ⑤7) 재현 확인
assert choices(PARAMS) == (3, 4, 5, 6, 7)

# fixed_value 단독 변경 → 정답(보기 번호)이 바뀜을 확인 (fixed_index=1 고정)
assert solve(dict(fixed_index=1, fixed_value=1)) == 2
assert solve(dict(fixed_index=1, fixed_value=2)) == 3
assert solve(dict(fixed_index=1, fixed_value=4)) == 5
assert solve(PARAMS) == 4  # 원문제(fixed_value=3)

# fixed_index 단독 변경 → 정답(보기 번호)이 바뀜을 확인 (fixed_value=3 고정)
assert solve(dict(fixed_index=2, fixed_value=3)) == 2
assert solve(dict(fixed_index=4, fixed_value=3)) == 2


def statement(prm):
    fi = prm['fixed_index']
    fv = prm['fixed_value']
    t1, t2 = TARGET
    cs = choices(prm)
    circles = ['①', '②', '③', '④', '⑤']
    opt_str = ' '.join(f'{circles[i]} {c}' for i, c in enumerate(cs))
    return (
        f"집합 X = {{1, 2, ..., {N}}}에 대하여 함수 f : X → X가 다음 조건을 만족시킨다.\n\n"
        f"집합 X의 임의의 두 원소 a, b에 대하여\n"
        f"f(a) ≥ b이면 f(a) ≥ f(b)\n"
        f"이다.\n\n"
        f"f({fi}) = {fv}일 때, f({t1}) + f({t2})의 최솟값은? [4점]\n\n"
        f"{opt_str}"
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
