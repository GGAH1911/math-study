from sympy import symbols, Eq, solve, Sum, Symbol
S1, S2 = symbols('S1 S2', real=True)
eq1 = Eq(4*S2 - 4*S1 + 5, 61)
eq2 = Eq(S2 - 4*S1, 11)
sol = solve([eq1, eq2], [S1, S2])
ans = 15
if sol[S2] == ans:
    # Also verify with explicit sample: find a 5-tuple satisfying S1, S2 and check originals
    # Use a_k all equal? S1=5a => a=1/5, S2=5a^2=1/5 ≠15. Use general sample.
    # Just check the algebraic identities with S1,S2 from solution.
    s1v = float(sol[S1]); s2v = float(sol[S2])
    lhs1 = 4*s2v - 4*s1v + 5
    lhs2 = s2v - 4*s1v
    if abs(lhs1 - 61) < 1e-9 and abs(lhs2 - 11) < 1e-9 and s2v == ans:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')
