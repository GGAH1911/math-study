"""2019 고3 4월모의고사 가형 9번 — 파라미터 솔버 (수동 작성).
문제: 자연수 7을 같은 자연수가 3개 이상 포함되도록 분할하는 방법의 수. (답 ③ 6)
구조: 7의 모든 분할 중, 어떤 값의 중복도(multiplicity)가 3 이상인 것을 센다.
      {4+1+1+1, 3+1+1+1+1, 2+2+2+1, 2+2+1+1+1, 2+1+1+1+1+1, 1×7} → 6가지.
재생산: (n, 최소중복도) 파라미터화.
"""
from collections import Counter


def count(n=7, min_mult=3):
    def parts(rem, mx):
        if rem == 0:
            yield ()
            return
        for k in range(min(rem, mx), 0, -1):
            for rest in parts(rem - k, k):
                yield (k,) + rest
    return sum(1 for p in parts(n, n) if max(Counter(p).values()) >= min_mult)


CANDIDATE = 6                       # 보기 ③
assert count() == CANDIDATE, count()
print('VERIFY_PASS')
