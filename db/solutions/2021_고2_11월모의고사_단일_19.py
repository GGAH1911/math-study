from sympy import *
n = symbols('n', positive=True, integer=True)

# 검증: p=2, f(n)=n+1, g(n)=n(n+1)이 올바른지 확인
p = 2
def f(n_val):
    return n_val + 1
def g(n_val):
    return n_val * (n_val + 1)

# n=1 검증: a_1 = p
a1 = p
T1 = (1 - Rational(1,2)) * a1
assert T1 == 1, f'T_1 should be 1, got {T1}'

# n=2 검증: 원래 조건 확인
a2_sum = (2*2 - 1) * 2 * 3  # Σa_k = (2n-1)×n(n+1)
a2 = a2_sum - a1
T2_calc = (Rational(1,1) - Rational(1,3))*a1 + (Rational(1,2) - Rational(1,3))*a2
assert T2_calc == 4, f'T_2 should be 4, got {T2_calc}'

# n=3 검증
a3_sum = (2*3 - 1) * 3 * 4
a3 = a3_sum - (a1 + a2)
T3_calc = (1 - Rational(1,4))*a1 + (Rational(1,2) - Rational(1,4))*a2 + (Rational(1,3) - Rational(1,4))*a3
assert T3_calc == 9, f'T_3 should be 9, got {T3_calc}'

# 최종 답 계산
result = f(2*p) * g(3*p)
assert result == 210, f'f(2p)×g(3p) should be 210, got {result}'

print('VERIFY_PASS')