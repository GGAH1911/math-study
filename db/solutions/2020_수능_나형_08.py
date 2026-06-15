# 2020 수능 나형 08 (그래프): lim_{x→0+}f(x) - lim_{x→1-}f(x)?  (보기 ①=-2)
# 그래프 판독: 0<x<1 에서 (0,0)→(1,2) 직선 y=2x (양 끝 개원). 두 극한은 이 직선의 끝값.
CANDIDATE = -2
def rising(x):
    return 2 * x                  # (0,0)→(1,2)
L0 = rising(0)                    # lim_{x→0+} f(x) = 0
L1 = rising(1)                    # lim_{x→1-} f(x) = 2
print('VERIFY_PASS' if L0 - L1 == CANDIDATE else 'VERIFY_FAIL')
