import sympy as sp

a = 4
# choose n=1 (arbitrary, area must be 3/2 for any valid n with m=4n)
n = sp.Rational(1)
m = 4*n

# Intersection of y=a/x and y=mx → P
xP = sp.sqrt(sp.Rational(a, 1) / m)
yP = m * xP

# Intersection of y=a/x and y=nx → Q
xQ = sp.sqrt(sp.Rational(a, 1) / n)
yQ = n * xQ

# R: vertical line x=xP meets y=nx
xR = xP
yR = n * xR

# Check condition: xQ = 2*xP
cond1 = sp.simplify(xQ - 2*xP) == 0

# Area of triangle PRQ
base = yP - yR  # |PR| vertical
height = xQ - xP  # horizontal distance from Q to line x=xP
area = sp.Rational(1,2) * base * height
cond2 = sp.simplify(area - sp.Rational(3,2)) == 0

# Check that P and Q are on hyperbola y=a/x
cond3 = sp.simplify(yP - a/xP) == 0
cond4 = sp.simplify(yQ - a/xQ) == 0

if cond1 and cond2 and cond3 and cond4:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL cond1={cond1} cond2={cond2} area={area} xQ={xQ} 2xP={2*xP}')
