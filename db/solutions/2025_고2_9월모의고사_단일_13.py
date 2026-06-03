from sympy import *
a = symbols('a', positive=True)
# a=2로 구체적 검증
a_val = 2
b_val = a_val ** Rational(3, 2)  # log_a(b) = 3/2
c_val = a_val ** 3               # log_a(c) = 3

# 조건1: a^3 == b^2
cond1 = abs(a_val**3 - b_val**2) < 1e-9

# 조건2: log_a(c) == log_b(c) + 1
log_a_c = log(c_val) / log(a_val)
log_b_c = log(c_val) / log(b_val)
cond2 = abs(log_a_c - (log_b_c + 1)) < 1e-9

# 답 검증: log_c(ab)
result = log(a_val * b_val) / log(c_val)
expected = Rational(5, 6)
cond3 = abs(float(result) - float(expected)) < 1e-9

if cond1 and cond2 and cond3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', cond1, cond2, cond3)
