from sympy import *
a = 2
xA = 4
yA = Rational(1,2) * xA
print(f'Point A: ({xA}, {yA})')

# Verify A is on both curves
lhs1 = log(xA - a, sqrt(2))
rhs1 = Rational(1,2) * xA
print(f'A on log curve: {simplify(lhs1)} = {rhs1}, Equal: {simplify(lhs1 - rhs1) == 0}')

# Line through A with slope -1
xB = 2
yB = -xB + (Rational(3,2) * xA)
print(f'Point B from line: ({xB}, {yB})')

# Verify B is on exponential curve
lhs2 = yB
rhs2 = (sqrt(2))**xB + a
print(f'B on exponential curve: {lhs2} = {simplify(rhs2)}, Equal: {simplify(lhs2 - rhs2) == 0}')

# Verify triangle area
area = abs(xA * yB - yA * xB) / 2
print(f'Triangle OAB area: {area}')
if area == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')