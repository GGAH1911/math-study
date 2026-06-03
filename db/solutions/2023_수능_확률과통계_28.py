from sympy import *

a_val = Rational(4)
b_val = Rational(5, 2)
c_val = Rational(1, 2)

x = symbols('x', real=True)

# PDF: 증가 구간 [0,b], 감소 구간 [b,a]
f1 = c_val / b_val * x          # 0 <= x <= b
f2 = c_val / (a_val - b_val) * (a_val - x)  # b <= x <= a

# 1. 전체 넓이 = 1
total = integrate(f1, (x, 0, b_val)) + integrate(f2, (x, b_val, a_val))
assert total == 1, f'Total area = {total}'

# 2. P(X<=b) - P(X>=b) = 1/4
p_leq_b = integrate(f1, (x, 0, b_val))
p_geq_b = integrate(f2, (x, b_val, a_val))
assert p_leq_b - p_geq_b == Rational(1, 4), f'Diff = {p_leq_b - p_geq_b}'

# 3. P(X <= sqrt(5)) = 1/2  (sqrt(5) < b 이므로 f1 구간)
p_leq_sqrt5 = integrate(f1, (x, 0, sqrt(5)))
assert p_leq_sqrt5 == Rational(1, 2), f'P(X<=sqrt5) = {p_leq_sqrt5}'

# 4. 최종 답 검증
result = a_val + b_val + c_val
assert result == 7, f'a+b+c = {result}'

print('VERIFY_PASS')
