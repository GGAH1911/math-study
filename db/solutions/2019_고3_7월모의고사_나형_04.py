"""2019 고3 7월모의고사 나형 4번 — 파라미터 솔버 (수동).
그림 대응 f: 1→4, 2→3, 3→2, 4→5.  f(2)+f⁻¹(3)=3+2=5. (답 ③, 값 5)"""
def solve(f, a, binv):
    finv = {v:k for k,v in f.items()}
    return f[a] + finv[binv]
F = {1:4, 2:3, 3:2, 4:5}
assert solve(F, 2, 3) == 5
print('VERIFY_PASS')
