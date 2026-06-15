"""2019 고3 7월모의고사 나형 30번 — 파라미터 솔버 (수동).
삼차 f, 극값 x=-3,a(a>-3). g=f(x<-3), ∫₀ˣ|f'|(x≥-3). g(-3)=-16,g(a)=-8, 연속, 극솟값 존재.
조건서: c<0(극솟값 위해), 연속 f(-3)=-16, 부호적분으로 f(a)=-8,f(0)=-16,a=-1 → f=-2x³-12x²-18x-16.
[-1,4]서 f'<0 → g=∫₀ˣ|f'|=f(0)-f(x)=-16-f(x) → f+g=-16(상수). |∫₋₁⁴(f+g)dx|=|-16·5|=80."""
import sympy as sp
def solve():
    x,c,a,d=sp.symbols('x c a d',real=True)
    f=c*(x**3/3+(3-a)*x**2/2-3*a*x)+d        # ∫f' , f'=c(x+3)(x-a)
    sol=sp.solve([f.subs(x,0)+16, f.subs(x,-3)+16, f.subs(x,-1)+8],[c,a,d],dict=True)
    s=[t for t in sol if t[a]>-3][0]
    fx=f.subs(s)
    fp=sp.diff(fx,x)
    a0=s[a]
    # [-1,4]: g=∫₀ˣ|f'| ; f'<0 이므로 g=-(f(x)-f(0))=f(0)-f(x)
    g=fx.subs(x,0)-fx
    integ=sp.integrate(fx+g,(x,a0,4))
    return abs(integ)
assert solve()==80, solve()
print('VERIFY_PASS')
