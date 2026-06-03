from sympy import *
x, a_sym = symbols('x a')
f = x**3 - 6*x**2 + 8*x + 1
fp = diff(f, x)

# k=3 확인
k = 3
condition = (1 - f.subs(x, k)) + k * fp.subs(x, k)
assert condition == 0, f'k=3 접선 조건 실패: {condition}'

# 직선 AB
line = -x + 1
assert f.subs(x, 0) == 1 and line.subs(x, 0) == 1, 'A(0,1) 불일치'
assert f.subs(x, 3) == -2 and line.subs(x, 3) == -2, 'B(3,-2) 불일치'

# S1 계산
S1 = integrate(f - line, (x, 0, 3))
assert S1 == Rational(27, 4), f'S1 실패: {S1}'

# g(x) with a=3/2
a_val = Rational(3, 2)
b_val = -1 - 3*a_val  # = -11/2
g = a_val*x**2 + b_val*x + 1
assert g.subs(x, 0) == 1, 'g(0)!=1'
assert g.subs(x, 3) == -2, 'g(3)!=-2'
assert a_val > 0, '최고차항 계수 양수 조건 실패'

# S2 계산
S2 = integrate(line - g, (x, 0, 3))  # g < line on (0,3)
assert S2 > 0, f'S2 음수: {S2}'
assert S1 == S2, f'S1={S1}, S2={S2} 불일치'

# 최종 적분
result = integrate(g, (x, 0, 3))
assert result == Rational(-33, 4), f'최종 적분 실패: {result}'

print('VERIFY_PASS')
