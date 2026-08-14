# 2026 고3 7월 확률과통계 28 — 파라미터화 솔버
#
# 유형: 빈 상자 boxes 개에 검은 공 black 개, 흰 공 white 개를 남김없이 분배
#       (같은 색끼리는 구별하지 않음, 빈 상자 허용).
#   (가) 검은 공이 들어 있지 않은 상자의 개수는 min_black_free 이상이다.
#   (나) 검은 공이 들어 있는 상자에 들어 있는 흰 공의 개수는 max_white 이하이다.
#
# 세는 방법 (검은 공이 든 상자 개수 k 로 분류):
#   · 검은 공 배치: 상자 k 개를 고르고(C(boxes,k)) 그 k 개에 black 개를 양의 정수로 쪼갠다
#     (C(black-1, k-1) = 중복조합/조합론의 막대와 칸막이).  (가) ⇔ boxes - k >= min_black_free
#   · 흰 공 배치: k 개 상자는 max_white 이하, 나머지 boxes-k 개는 제한 없음
#     → 포함배제로 센다.  (나)
import sympy as sp

CANDIDATE = 5                 # 정답: 보기 ⑤ (= 628가지)

PARAMS = dict(
    boxes=4,                  # 상자 개수
    black=4,                  # 검은 공 개수
    white=6,                  # 흰 공 개수
    min_black_free=2,         # (가) 검은 공이 없는 상자 개수의 하한
    max_white=1,              # (나) 검은 공이 든 상자에 허용되는 흰 공 개수 상한
    choices=(580, 592, 604, 616, 628),   # 보기 (정답 번호는 solve 가 대조해서 정한다)
)


def _weak(total, parts):
    """합이 total 인 음이 아닌 정수해 (x1..x_parts) 의 개수 = C(total+parts-1, parts-1)."""
    if parts <= 0:
        return 1 if total == 0 else 0
    return int(sp.binomial(total + parts - 1, parts - 1))


def _white_ways(white, boxes, k, cap):
    """흰 공 white 개를 boxes 개 상자에 분배: 지정된 k 개 상자는 cap 이하, 나머지는 제한 없음.
    '어떤 상자가 cap 을 넘는다' 를 포함배제로 뺀다."""
    tot = 0
    for i in range(k + 1):
        rest = white - i * (cap + 1)
        if rest < 0:
            break
        tot += (-1) ** i * int(sp.binomial(k, i)) * _weak(rest, boxes)
    return tot


def count_ways(prm):
    """조건 (가),(나) 를 만족하는 (검은 공 분배, 흰 공 분배) 쌍의 개수."""
    n, B, W = prm['boxes'], prm['black'], prm['white']
    cap, free = prm['max_white'], prm['min_black_free']
    total = 0
    for k in range(0, n + 1):                       # k = 검은 공이 들어 있는 상자의 개수
        if n - k < free:                            # (가) 검은 공 없는 상자 >= free
            continue
        if k == 0:
            black_ways = 1 if B == 0 else 0
        else:
            black_ways = int(sp.binomial(n, k)) * int(sp.binomial(B - 1, k - 1))
        if black_ways == 0:
            continue
        total += black_ways * _white_ways(W, n, k, cap)
    return total


def solve(prm):
    """조건 → 답(보기 번호). 보기에 없는 값이면 0 (= 대응하는 보기 없음)."""
    val = count_ways(prm)
    ch = list(prm['choices'])
    return ch.index(val) + 1 if val in ch else 0


def brute(prm):
    """작은 경우의 독립 대조용 완전열거 (구조식이 맞는지 확인)."""
    n, B, W = prm['boxes'], prm['black'], prm['white']
    cap, free = prm['max_white'], prm['min_black_free']

    def comps(total, parts):
        if parts == 1:
            yield (total,); return
        for first in range(total + 1):
            for rest in comps(total - first, parts - 1):
                yield (first,) + rest

    cnt = 0
    for b in comps(B, n):
        if sum(1 for x in b if x == 0) < free:
            continue
        for w in comps(W, n):
            if all(w[i] <= cap for i in range(n) if b[i] >= 1):
                cnt += 1
    return cnt


def make_choices(prm, step=12, pos=5):
    """유사문제용 보기 생성: 참값을 pos 번째로 두고 step 간격의 등차 보기 5개."""
    val = count_ways(prm)
    return tuple(val + (i - pos) * step for i in range(1, 6))


def statement(prm):
    """새 문제 문장."""
    ch = prm['choices']
    return (
        f"빈 상자 {prm['boxes']}개가 일렬로 놓여 있고, 검은 공 {prm['black']}개, "
        f"흰 공 {prm['white']}개가 있다. 이 {prm['black'] + prm['white']}개의 공을 상자에 "
        "남김없이 나누어 넣을 때, 다음 조건을 만족시키는 경우의 수는? "
        "(단, 같은 색 공끼리는 서로 구별하지 않고, 공이 들어 있지 않은 상자가 있을 수 있다.)\n"
        f"(가) 검은 공이 들어 있지 않은 상자의 개수는 {prm['min_black_free']} 이상이다.\n"
        f"(나) 검은 공이 들어 있는 상자에 들어 있는 흰 공의 개수는 {prm['max_white']} 이하이다.\n"
        + "  ".join(f"{'①②③④⑤'[i]} {ch[i]}" for i in range(5))
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
