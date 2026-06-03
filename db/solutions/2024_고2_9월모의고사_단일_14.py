import numpy as np

def real_nth_roots_count(a, n):
    # number of real n-th roots of real a
    # equation x^n = a, count real solutions
    # use sympy to be safe
    from sympy import symbols, solve, Rational, I, simplify, nsimplify, Integer
    x = symbols('x')
    sols = solve(x**n - a, x)
    count = 0
    for s in sols:
        if s.is_real:
            count += 1
    return count

total = 0
matches = []
for n in range(2, 11):
    a1 = n*n + 1
    a2 = n*n - 8*n + 12
    f = real_nth_roots_count(a1, n)
    g = real_nth_roots_count(a2, n)
    if f == 2*g:
        matches.append(n)
        total += n

if total == 8 and matches == [2, 6]:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', matches, total)
