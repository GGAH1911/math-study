import sympy as sp

CANDIDATE = 9

# 등비수열 설정
a1 = sp.Rational(1, 3)
r = 3

# a_4 검증
a4 = a1 * r**3
if a4 == CANDIDATE:
    # 원래 조건식 검증: S_{n+3} - S_n = 13 * 3^{n-1}
    def verify_condition(n_val):
        S_n = a1 * (r**n_val - 1) / (r - 1)
        S_n3 = a1 * (r**(n_val + 3) - 1) / (r - 1)
        diff = S_n3 - S_n
        expected = 13 * 3**(n_val - 1)
        return sp.simplify(diff - expected) == 0
    
    # n = 1, 2, 3에서 검증
    if all(verify_condition(n) for n in [1, 2, 3]):
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')