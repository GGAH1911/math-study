import sympy as sp
# OA=OB=1,∠AOB=θ 이등변. AB지름 반원이 OA,OB와 P,Q. M=AB중점, 부채꼴 MPQ 넓이 S(θ).
# (가)MA=sin(θ/2)=f, (나)∠AMP=θ=g, (다)∠PMQ=π-2θ=h. f(π/3)g(π/6)/h(π/4)? (④=1/6)
CANDIDATE = sp.Rational(1, 6)
f = lambda t: sp.sin(t/2)
g = lambda t: t
h = lambda t: sp.pi - 2*t
val = f(sp.pi/3)*g(sp.pi/6)/h(sp.pi/4)
print('VERIFY_PASS' if sp.simplify(val - CANDIDATE) == 0 else 'VERIFY_FAIL')
