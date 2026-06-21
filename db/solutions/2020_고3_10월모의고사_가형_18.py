import sympy as sp

r = 2
area_semi = sp.Rational(1,2)*sp.pi*r**2          # 2*pi
s2 = sp.sqrt(2)
area_rect = (2*s2)*s2                            # rectangle width 2*sqrt2, height sqrt2 = 4
area_tri = sp.Rational(1,2)*4*2                  # triangle base 4, height 2 = 4

# rectangle in -s2<=x<=s2, 0<=y<=s2 ; triangle: 0<=y<=2-|x|
# intersection area = integral over x of min(s2, 2-|x|)
x = sp.symbols('x', real=True)
xb = 2 - s2                                       # breakpoint where 2-x = sqrt2
I1 = sp.integrate(s2, (x, 0, xb))
I2 = sp.integrate(2 - x, (x, xb, s2))
area_rt = sp.simplify(2*(I1 + I2))               # = 8*sqrt2 - 8

area_union = area_rect + area_tri - area_rt       # 16 - 8*sqrt2
S1 = sp.simplify(area_semi - area_union)         # 2*pi + 8*sqrt2 - 16

# new diameter A2B2 = 2*sqrt2, original 4 -> area ratio = (2*sqrt2/4)^2 = 1/2
ratio = (2*s2/4)**2
S_inf = sp.simplify(S1/(1 - ratio))

claimed = 4*sp.pi + 16*sp.sqrt(2) - 32
if sp.simplify(ratio - sp.Rational(1,2)) == 0 and sp.simplify(S_inf - claimed) == 0 and S1 > 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
