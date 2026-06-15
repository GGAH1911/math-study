"""2019 고3 4월모의고사 나형 13번 — 파라미터 솔버 (수동 작성).
문제: X={2,4,6}, X→X 일대일대응 f,g. 그림의 f. 모든 k에 f(k)≠g(k), g(2)=6.
      f^{-1}(6)+g(4). (답 ② = 6)
그림 판독(f): f(2)=4, f(4)=6, f(6)=2 (3-순환).
구조: 제약 만족 g 를 전수 탐색(유일 결정: g(2)=6,g(4)=2,g(6)=4) → f^{-1}(6)=4, g(4)=2 → 6.
재생산: f 대응표 파라미터화.
"""
from itertools import permutations


def solve(f, g2, target):
    X = sorted(f)
    results = set()
    for perm in permutations(X):                 # g: 일대일대응 전수
        g = dict(zip(X, perm))
        if g[2] != g2:
            continue
        if any(g[k] == f[k] for k in X):          # 모든 k: f(k)≠g(k)
            continue
        finv = {v: k for k, v in f.items()}        # f^{-1}
        results.add(finv[6] + g[4])
    assert len(results) == 1, results             # 유일 결정 확인
    return results.pop()


F = {2: 4, 4: 6, 6: 2}      # 그림에서 읽은 대응
CANDIDATE = 6               # 보기 ② 의 값
assert solve(F, 6, CANDIDATE) == CANDIDATE
print('VERIFY_PASS')
