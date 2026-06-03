from sympy import symbols, solve, Rational, sqrt, simplify
a1, r = symbols('a1 r', positive=True)
sol = solve([a1*r**2 - 6, a1*r**5 - 3*a1*r**3], [a1, r], dict=True)
ok = False
for s in sol:
    a1v = s[a1]; rv = s[r]
    if a1v > 0 and rv > 0:
        a3 = a1v * rv**2
        a4 = a1v * rv**3
        a6 = a1v * rv**5
        a9 = a1v * rv**8
        if simplify(a3 - 6) == 0 and simplify(a6 - 3*a4) == 0 and simplify(a9 - 162) == 0:
            ok = True
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')