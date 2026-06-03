from sympy import symbols, log, Rational, solve, simplify, sqrt
a, b = symbols('a b', positive=True)
eq1 = log(a**2, 3) - 4
eq2 = log(a*b, 9) - Rational(5, 2)
sol = solve([eq1, eq2], [a, b], dict=True)
ok = False
for s in sol:
    A, B = s[a], s[b]
    if simplify(log(A**2, 3) - 4) == 0 and simplify(log(A*B, 9) - Rational(5, 2)) == 0:
        ratio = simplify(B / A)
        if ratio == 3:
            ok = True
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')