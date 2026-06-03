import sympy as sp
x = sp.Symbol('x')
# 원래 도함수
f_prime = 3*x**2 - 5
# 부정적분으로 f(x) 구하기
f = sp.integrate(f_prime, x) + 1  # 초기조건 f(0)=1 적용
# f(x) = x^3 - 5x + 1
# 검증: f'(x) 확인
f_check = x**3 - 5*x + 1
derivative = sp.diff(f_check, x)
assert derivative == f_prime, 'Derivative mismatch'
# 초기조건 확인
assert f_check.subs(x, 0) == 1, 'Initial condition failed'
# f(1) 계산
result = f_check.subs(x, 1)
assert result == -3, f'Result mismatch: expected -3, got {result}'
print('VERIFY_PASS')