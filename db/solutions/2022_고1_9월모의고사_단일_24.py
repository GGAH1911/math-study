import sympy as sp
k = sp.Symbol('k', integer=True)
x = sp.Symbol('x')

# 판별식 계산
discriminant = (k+2)**2 - 4*(1)*(k+5)
discriminant_simplified = sp.expand(discriminant)
print(f'판별식: {discriminant_simplified}')

# D < 0 조건
inequality = discriminant_simplified < 0
solution_set = sp.solve(inequality, k)
print(f'D < 0의 해: {solution_set}')

# 정수 k 개수
integers_in_range = [i for i in range(-4, 5) if -4 < i < 4]
print(f'범위 -4 < k < 4를 만족하는 정수: {integers_in_range}')
print(f'개수: {len(integers_in_range)}')

# 검증: 각 정수에 대해 판별식 확인
for k_val in integers_in_range:
    D_val = k_val**2 - 16
    print(f'k={k_val}: D = {D_val} (음수: {D_val < 0})')

# 최종 답
answer = len(integers_in_range)
print(f'\nVERIFY_PASS' if answer == 7 else 'VERIFY_FAIL')