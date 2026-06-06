import sympy as sp

a = sp.Symbol('a', integer=True, positive=True)
x = sp.Symbol('x')

# 원래 이차방정식
eq = x**2 + 2*a*x + a**2 + 4*a - 28

# 판별식
discriminant = (2*a)**2 - 4*(a**2 + 4*a - 28)
discriminant_simplified = sp.expand(discriminant)
print(f'판별식: {discriminant_simplified}')

# 실근 조건
print(f'\n실근 조건: {discriminant_simplified} >= 0')

# 자연수 a에 대해 판별식 값 확인
print(f'\n자연수 a에 대한 판별식 값:')
valid_a = []
for a_val in range(1, 15):
    d_val = -16*a_val + 112
    if d_val >= 0:
        valid_a.append(a_val)
    print(f'a = {a_val}: D = {d_val}', '✓' if d_val >= 0 else '✗')

print(f'\n조건을 만족하는 자연수 a: {valid_a}')
print(f'개수: {len(valid_a)}')

if len(valid_a) == 7:
    print('\nVERIFY_PASS')
else:
    print('\nVERIFY_FAIL')