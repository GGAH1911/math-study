import sympy as sp
x, a = sp.symbols('x a')

# a = -2일 때 f(x) 정의
f = -3*x**2 + 12*x + 16

# 첫 번째 조건: f(x)를 (x+2)^2으로 나눈 나머지
q1, r1 = sp.div(f, (x+2)**2)
remainder_check = 2*f + 6*x**2 - 4
remainder_check_simplified = sp.expand(remainder_check)
print(f'Remainder from division: {r1}')
print(f'Expected remainder form: {remainder_check_simplified}')
assert r1 == sp.expand(remainder_check), 'First condition failed'

# 두 번째 조건: {f(x)}^2 - 2f(x) + 3을 x^2-4x-5로 나눈 나머지
g = f**2 - 2*f + 3
q2, r2 = sp.div(g, x**2 - 4*x - 5)
print(f'Remainder of g(x): {r2}')
assert r2 == 2, 'Second condition failed'

# f(a^2) = f(4) 계산
result = f.subs(x, 4)
print(f'f(4) = {result}')
assert result == 16, 'Final answer verification failed'
print('VERIFY_PASS')