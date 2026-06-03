from sympy import *

p_val = sqrt(3)
k_val = Rational(5,1)*sqrt(3)/9

# Points
xA = k_val * pi/3
xB = k_val * 4*pi/3
xC = k_val * 2*pi/3
yA = p_val
yB = p_val
yC = -p_val

# Verify original equation f(x)=tan(x/k) at each point
assert simplify(tan(xA/k_val) - p_val) == 0, 'f(A)!=p'
assert simplify(tan(xB/k_val) - p_val) == 0, 'f(B)!=p'
assert simplify(tan(xC/k_val) + p_val) == 0, 'f(C)!=-p'

# Verify AB = 3*PA
PA_d = xA
AB_d = xB - xA
assert simplify(AB_d - 3*PA_d) == 0, 'AB!=3*PA'
assert PA_d < xB, 'PA<PB violated'

# Domain check
assert 0 <= xA and simplify(xA - k_val*pi/2) < 0, 'A domain fail'
assert simplify(xB - k_val*pi/2) > 0 and simplify(xB - 3*k_val*pi/2) < 0, 'B domain fail'
assert simplify(xC - k_val*pi/2) > 0 and simplify(xC - k_val*pi) < 0, 'C domain fail'

# Area of triangle OCB (shoelace with O=origin)
area = Rational(1,2) * (xC*yB - yC*xB)
assert simplify(area - Rational(5)*pi/3) == 0, f'Area!=5pi/3, got {simplify(area)}'

# k+p
kp = simplify(k_val + p_val)
expected = 14*sqrt(3)/9
if simplify(kp - expected) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: k+p={kp}, expected {expected}')
