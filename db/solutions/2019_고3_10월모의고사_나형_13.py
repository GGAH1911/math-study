"""2019 고3 10월모의고사 나형 13번 — 파라미터 솔버 (수동).
f 기함수(연속), g(x)=f(x-1)+1 (우1·상1 평행이동). ∫₀² g dx. (답 ② 2)
∫₀²g=∫₀²[f(x-1)+1]dx=∫₋₁¹f(u)du+2=0+2=2 (기함수라 ∫₋₁¹f=0). f 무관."""
import sympy as sp
def solve():
    u=sp.symbols('u')
    # 기함수면 ∫_{-1}^{1}f=0 (임의 기함수로 확인)
    f=u**3-sp.sin(u)                           # 임의 기함수 예
    return sp.integrate(f,(u,-1,1))+2
assert solve()==2
print('VERIFY_PASS')
