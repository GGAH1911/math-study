import sympy as sp

theta = sp.symbols('theta', real=True)
cos_t, sin_t = sp.symbols('cos_t sin_t', real=True)

# equation: 2*cos(theta) + cos(pi/2 - theta) = 0 -> cos(pi/2-theta)=sin(theta)
# so 2*cos_t + sin_t = 0, sin_t = -2*cos_t
# with sin_t^2+cos_t^2=1
sols = sp.solve([sp.Eq(sin_t, -2*cos_t), sp.Eq(sin_t**2+cos_t**2,1)], [sin_t, cos_t])

answer = None
for s in sols:
    sin_v, cos_v = s[0], s[1]
    if sin_v < 0:
        answer = cos_v

expected = sp.sqrt(5)/5
if sp.simplify(answer - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
