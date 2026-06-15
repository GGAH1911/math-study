"""2019 고3 4월모의고사 가형 28번 — 파라미터 솔버 (수동 작성).
문제: 5명(할아버지GF·할머니GM·아버지F·어머니M·아이C). 2열 좌석(A:앞=스크린쪽, B:뒤),
      각 열 5석, 같은 column 으로 정렬. A열: GF,GM 이웃. B열: F,M,C 앉되 C는 F 또는 M과
      이웃, '아이 바로 앞 좌석'(=같은 column 의 A석)은 비어 있음. 경우의 수. (답 192)
구조: A에 GF,GM 인접배치(순서) × B에 F,M,C 배치(C가 F/M과 인접) 단, C의 column ∉ {GF,GM의 column}
      (아이 앞 A석이 비어야 하므로).
재생산: 열 길이 ncols 파라미터화.
"""
from itertools import permutations


def count(ncols=5):
    cols = list(range(1, ncols + 1))
    total = 0
    for gf, gm in permutations(cols, 2):              # A열: 할아버지·할머니 (사람 구분 → 순서)
        if abs(gf - gm) != 1:                          # 이웃
            continue
        A = {gf, gm}
        for f, m, c in permutations(cols, 3):          # B열: 아버지·어머니·아이
            if not (abs(c - f) == 1 or abs(c - m) == 1):   # 아이는 부 또는 모와 이웃
                continue
            if c in A:                                  # 아이 바로 앞(A석)이 비어야
                continue
            total += 1
    return total


CANDIDATE = 192
assert count(5) == CANDIDATE, count(5)
print('VERIFY_PASS')
