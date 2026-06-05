import sympy as sp

# 원래 조건: sum_{k=1}^{n} a_k/(k-1)! = 3/(n+2)!
# a_1 = 1/2
# a_n = -3/(n(n+2)) for n >= 2

a1 = sp.Rational(1, 2)

# 원래 조건 만족 여부 확인
def verify_original_condition():
    for n_test in range(1, 6):
        lhs = 0
        for k in range(1, n_test + 1):
            if k == 1:
                a_k = a1
            else:
                a_k = sp.Rational(-3, k * (k + 2))
            lhs += a_k / sp.factorial(k - 1)
        
        rhs = sp.Rational(3) / sp.factorial(n_test + 2)
        if sp.simplify(lhs - rhs) != 0:
            return False
    return True

# 극한값 계산
n = sp.Symbol('n', positive=True, integer=True)
a_n_formula = sp.Rational(-3) / (n * (n + 2))
limit_expr = a1 + n**2 * a_n_formula
limit_val = sp.limit(limit_expr, n, sp.oo)

if verify_original_condition() and limit_val == sp.Rational(-5, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')