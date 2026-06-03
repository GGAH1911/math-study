from sympy import symbols, I, expand, im, simplify, solve, Rational
a = symbols('a', real=True)
z = a**2 + (1+I)*a - 6*(2+I)
z2 = expand(z*z)
im_part = simplify(im(z2))
roots = solve(im_part, a)
real_roots = [r for r in roots if r.is_real]
total = sum(real_roots)
if total == 5:
    # verify each value makes z^2 real
    ok = True
    for r in real_roots:
        val = expand((r**2 + (1+I)*r - 6*(2+I))**2)
        if simplify(im(val)) != 0:
            ok = False
            break
    print('VERIFY_PASS' if ok else 'VERIFY_FAIL')
else:
    print('VERIFY_FAIL')
