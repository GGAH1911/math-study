"""2019 고3 10월모의고사 나형 24번 — 파라미터 솔버 (수동).
최고차1 이차 f, lim_{x→5}(f(x)-x)/(x-5)=8. 분모→0이라 f(5)=5, 극한=f'(5)-1=8→f'(5)=9.
f=x²+bx+c: 2·5+b=9→b=-1, 25-5+c=5→c=-15. f=x²-x-15, f(7)=27. (답 27)"""
import sympy as sp
def solve(x0, L, xq):
    x,b,c=sp.symbols('x b c'); f=x**2+b*x+c
    s=sp.solve([f.subs(x,x0)-x0, sp.diff(f,x).subs(x,x0)-1-L],[b,c])
    return f.subs(s).subs(x,xq)
assert solve(5,8,7)==27
print('VERIFY_PASS')
