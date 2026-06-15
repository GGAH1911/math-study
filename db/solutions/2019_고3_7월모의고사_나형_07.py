"""2019 고3 7월모의고사 나형 7번 — 파라미터 솔버 (수동).
그림: lim_{x→-2-}f=-1 (좌측 수평선), lim_{x→1+}f=3 (우측 하강선 시작). 합=2. (답 ②)"""
def solve(left_lim_m2, right_lim_p1): return left_lim_m2 + right_lim_p1
assert solve(-1, 3) == 2
print('VERIFY_PASS')
