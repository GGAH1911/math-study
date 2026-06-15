import sympy as sp
# f(x)=a sin(π/6(x-1))+b, f(0)=8, g(t)=#{0<x<t:|f|=4}, g(18)=5 → a=-8,b=4.
# g(α)=|a-b|=12 인 양수 α 의 최댓값?
CANDIDATE = 49
a, b = -8, 4
assert sp.simplify(a*sp.sin(sp.pi/6*(0-1)) + b - 8) == 0          # f(0)=8
# |f|=4: f=4→sin=0→x=1+6k ; f=-4→sin=1→x=4+12k
pts = sorted(set([1+6*k for k in range(0, 30)] + [4+12*k for k in range(0, 30)]))
g = lambda al: sum(1 for x in pts if 0 < x < al)
assert g(18) == 5                                                  # g(18)=5
target = abs(a-b)                                                  # 12
maxalpha = pts[target]                                             # 13번째 점 (미포함)
print('VERIFY_PASS' if g(maxalpha) == target and maxalpha == CANDIDATE else 'VERIFY_FAIL')
