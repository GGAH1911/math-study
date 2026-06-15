import sympy as sp
from math import isclose

xs = sp.Symbol('xs', real=True)
# Condition (gamma): base definition of f on [0,4]
base = sp.Piecewise(
    (sp.Integer(2), (xs >= 0) & (xs < 2)),
    (-2*xs + 6,     (xs >= 2) & (xs < 3)),
    (sp.Integer(0), (xs >= 3) & (xs <= 4)),
)

def f(val):
    # Condition (na): period 8  f(x)=f(x-8)  and even  f(-x)=f(x)
    t = val % 8          # fold by period into [0,8)
    if t >= 4:
        t -= 8           # into [-4,4)
    u = abs(t)           # evenness -> [0,4]
    return float(base.subs(xs, sp.Rational(u)))

def g(x, n):
    # given definition of g
    return (abs(x)/x + n) if x != 0 else n

def comp_constant(n):
    # (f o g)(x): g maps x<0 -> n-1, x=0 -> n, x>0 -> n+1; samples cover whole range of g
    vals = [f(g(x, n)) for x in (-1, 0, 1)]
    return isclose(vals[0], vals[1]) and isclose(vals[1], vals[2])

count = sum(1 for n in range(1, 61) if comp_constant(n))
CANDIDATE = 30
print('count =', count)
print('VERIFY_PASS' if count == CANDIDATE else 'VERIFY_FAIL')