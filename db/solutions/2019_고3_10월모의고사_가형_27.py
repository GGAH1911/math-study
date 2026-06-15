"""2019 고3 10월모의고사 가형 27번 — 파라미터 솔버 (수동).
AB 지름 원, P 위의 점, P 접선이 AB와 만나는 Q는 AB를 5:1 외분, BQ=√3. AP·AQ. (답 50)
BQ=|AB|/4=√3 → |AB|=4√3. A=(0,0),B=(4√3,0),Q=(5√3,0). 접점 P: OP⊥PQ 로 결정 → AP·AQ=50."""
import sympy as sp
def solve(BQ=sp.sqrt(3)):
    AB=4*BQ                                   # 외분 5:1 → BQ=|AB|/4
    A=sp.Matrix([0,0]); B=sp.Matrix([AB,0]); O=(A+B)/2; r=AB/2
    Q=sp.Matrix([sp.Rational(5,4)*AB,0])      # 5:1 외분
    x,y=sp.symbols('x y',real=True)
    P=sp.Matrix([x,y])
    eqs=[(P-O).dot(P-O)-r**2, (Q-P).dot(P-O)]  # 원 위 + 접선(OP⊥PQ)
    sol=[s for s in sp.solve(eqs,[x,y],dict=True) if s[y]!=0][0]
    AP=P.subs(sol)-A; AQ=Q-A
    return sp.simplify(AP.dot(AQ))
assert solve()==50, solve()
print('VERIFY_PASS')
