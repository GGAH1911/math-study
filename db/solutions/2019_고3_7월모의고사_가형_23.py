"""2019 고3 7월모의고사 가형 23번 — 파라미터 솔버 (수동).
sec θ=10 → tan²θ = sec²θ - 1 = 100 - 1 = 99. (답 99)"""
def solve(sec): return sec**2 - 1
assert solve(10) == 99
print('VERIFY_PASS')
