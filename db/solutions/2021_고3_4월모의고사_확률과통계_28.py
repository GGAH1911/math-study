#!/usr/bin/env python3
"""확통_28 역검산 — 불규칙 도로망 A→P→B 최단경로(도로 재사용 금지) 경우의 수.
그림의 도로망을 좌표 격자로 인코딩해 경우의 수를 독립적으로 재계산하고 답 94(보기 ⑤)와 대조.
핵심: 순진한 곱 7×16=112 에서, '한 번 지난 도로 재사용 금지'로 P 바로 아래 도로를
왕복하는 18가지를 제외 → edge-disjoint 최단경로쌍만 카운트해야 94 가 나온다."""
from collections import deque

edges = set()
def add(a, b):
    edges.add((a, b)); edges.add((b, a))
# 왼쪽 블록 cols0-1 rows0-3 (1×3)
for r in range(4): add((0, r), (1, r))
for c in (0, 1):
    for r in range(3): add((c, r), (c, r + 1))
# 상단 띠(다리) rows2-3 cols0-5 — 좌↔우 유일 통행로, P=(2,3) 아래 도로는 col2의 row2-3 뿐
for r in (2, 3):
    for c in range(5): add((c, r), (c + 1, r))
for c in range(6): add((c, 2), (c, 3))
# 오른쪽 블록 cols3-5 rows0-2 (2×2)
for r in range(3):
    add((3, r), (4, r)); add((4, r), (5, r))
for c in (3, 4, 5):
    for r in range(2): add((c, r), (c, r + 1))

A, P, B = (0, 0), (2, 3), (5, 0)
nbr = {}
for u, v in edges:
    nbr.setdefault(u, []).append(v)

def dist(s):
    d = {s: 0}; q = deque([s])
    while q:
        u = q.popleft()
        for v in nbr[u]:
            if v not in d:
                d[v] = d[u] + 1; q.append(v)
    return d

def paths(s, t):
    dd = dist(s); out = []
    def rec(u, ed):
        if u == t:
            out.append(frozenset(ed)); return
        for v in nbr[u]:
            if dd[v] == dd[u] + 1:                 # 최단 방향으로만 전진
                rec(v, ed + [frozenset((u, v))])
    rec(s, []); return out

AP, PB = paths(A, P), paths(P, B)
cnt = sum(1 for a in AP for b in PB if not (a & b))   # 도로 재사용 금지 → edge-disjoint 쌍만
print('VERIFY_PASS' if cnt == 94 else f'VERIFY_FAIL(got {cnt}, AP={len(AP)}, PB={len(PB)})')
