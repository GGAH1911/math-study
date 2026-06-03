from sympy import symbols, sqrt, oo, limit, Rational, simplify
import numpy as np

# 원래 부등식: a_n^2 < 4*n*a_n + n - 4*n^2
# 변환: (a_n - 2n)^2 < n

# 1) 대수적 변환 검증 (sympy)
n_sym = symbols('n', positive=True)
a_sym = symbols('a')
original_ineq_lhs = a_sym**2 - 4*n_sym*a_sym - n_sym + 4*n_sym**2
factored = simplify(original_ineq_lhs - ((a_sym - 2*n_sym)**2 - n_sym))
assert factored == 0, 'factoring error'

# 2) 샌드위치 정리: 상한·하한 극한 = 5/2
upper = (5*n_sym + sqrt(n_sym)) / (2*n_sym + 4)
lower = (5*n_sym - sqrt(n_sym)) / (2*n_sym + 4)
upper_lim = limit(upper, n_sym, oo)
lower_lim = limit(lower, n_sym, oo)
target = Rational(5, 2)

# 3) 수치 검증: 제약을 만족하는 여러 수열에서 수렴 확인
err_bound = 1e-6
passed = True
for n_val in [10**4, 10**5, 10**6, 10**7]:
    for a_n in [2*n_val,                          # 중심
                2*n_val + np.sqrt(n_val) - 1,    # 상한 근방
                2*n_val - np.sqrt(n_val) + 1]:   # 하한 근방
        # 원래 부등식 만족 확인
        assert a_n**2 < 4*n_val*a_n + n_val - 4*n_val**2, f'constraint violated at n={n_val}'
        val = (a_n + 3*n_val) / (2*n_val + 4)
        if abs(val - 2.5) > 0.01:
            passed = False

if upper_lim == target and lower_lim == target and passed:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')