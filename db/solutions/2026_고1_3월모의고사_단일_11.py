import sympy as sp

# Given
AB = sp.Integer(10)
Area_ABC = sp.Integer(30)
BD = sp.Integer(4)

# Compute BC from area: (1/2)*AB*BC = 30
BC = 2 * Area_ABC / AB  # = 6
DC = BC - BD            # = 2

# Coordinates: B=(0,0), A=(0,10), D=(BD,0), C=(BC,0)
# Rotation axis: y-axis (line AB)

# Volume = Large cone - Small cone
# Large cone: apex A(0,10), base radius BC=6, height AB=10
# Small cone: apex A(0,10), base radius BD=4, height AB=10
Vol_large = sp.Rational(1,3) * sp.pi * BC**2 * AB
Vol_small = sp.Rational(1,3) * sp.pi * BD**2 * AB
Vol = Vol_large - Vol_small

# Also verify with washer method
y = sp.Symbol('y')
R = BC * (1 - y/AB)   # outer radius: line AC
r = BD * (1 - y/AB)   # inner radius: line AD
Vol_washer = sp.pi * sp.integrate(R**2 - r**2, (y, 0, AB))

expected = sp.Rational(200, 3) * sp.pi

if sp.simplify(Vol - expected) == 0 and sp.simplify(Vol_washer - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Cone method: {Vol}')
    print(f'Washer method: {Vol_washer}')
    print(f'Expected: {expected}')
