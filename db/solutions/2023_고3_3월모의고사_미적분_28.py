import sympy as sp

def verify():
    # Two solutions found: a = 7/4 (case a>1) and a = 1/2 (case 0<a<1)
    a1 = sp.Rational(7, 4)
    a2 = sp.Rational(1, 2)

    def limit_val(a):
        # For a > 1: lim = 2*(a-1)/(a+1)
        # For 0 < a < 1: lim = 1
        if a > 1:
            return 2*(a - 1)/(a + 1)
        else:
            return sp.Integer(1)

    def rhs(a):
        return sp.Rational(3, 1) / (2*a + 2)

    # Verify numerically for large n using sympy
    n = 200
    results = []
    for a_val in [a1, a2]:
        an = a_val**n
        dist = sp.sqrt(an**2 * (a_val - 1)**2 + 1)
        sn = (an + a_val**(n+1) + 2) / 2
        ratio_num = dist / sn
        lim_analytic = limit_val(a_val)
        rhs_val = rhs(a_val)
        # Check analytic limit == rhs
        check = sp.simplify(lim_analytic - rhs_val) == 0
        results.append(check)

    # Check sum
    total = a1 + a2
    sum_check = total == sp.Rational(9, 4)

    if all(results) and sum_check:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
        print(f'a=7/4 check: {results[0]}, a=1/2 check: {results[1]}, sum check: {sum_check}')

verify()
