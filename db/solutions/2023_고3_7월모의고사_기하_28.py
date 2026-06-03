import sympy as sp

a2 = sp.Integer(5)
b2 = sp.Integer(40)
c2 = sp.Integer(45)
a = sp.sqrt(a2)
b = sp.sqrt(b2)
c = sp.sqrt(c2)

# Foci and center
F = (c, sp.Integer(0))
Fp = (-c, sp.Integer(0))
A = (sp.Integer(0), sp.Integer(6))

# P coordinates
xP = 7*a2/c
yP = (25*a2 - c2)/sp.Integer(6)

# Check P on hyperbola
hyp = sp.simplify(xP**2/a2 - yP**2/b2)
assert hyp == 1, f'P not on hyperbola: {hyp}'

# Check P on circle centered at A
PA2 = sp.simplify(xP**2 + (yP - 6)**2)
assert PA2 == c2 + 36, f'P not on circle: {PA2}'

# Check PF:PF' = 3:4
PF = sp.sqrt((xP - c)**2 + yP**2)
PFp = sp.sqrt((xP + c)**2 + yP**2)
ratio = sp.simplify(PF/PFp)
assert ratio == sp.Rational(3,4), f'ratio wrong: {ratio}'

# Q coordinates
s2 = (36 - c2)/(c2 + 36)
xQ = s2*c
yQ = sp.Integer(12)*c2/(c2 + 36)

# Q in second quadrant
assert sp.simplify(xQ) < 0, 'xQ not negative'
assert sp.simplify(yQ) > 0, 'yQ not positive'

# angle F'QF = pi/2: Q on circle x^2+y^2=c^2
circle_check = sp.simplify(xQ**2 + yQ**2 - c2)
assert circle_check == 0, f'angle condition fail: {circle_check}'

# Q on line AF
y_AF = 6 - (sp.Integer(6)/c)*xQ
assert sp.simplify(y_AF - yQ) == 0, 'Q not on AF'

# Q on line PF'
slope = yP/(xP + c)
y_PFp = slope*(xQ + c)
assert sp.simplify(y_PFp - yQ) == 0, 'Q not on PF prime'

# Final answer
result = b2 - a2
assert result == 35, f'b^2-a^2 = {result}'

print('VERIFY_PASS')
