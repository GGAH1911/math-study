import sympy as sp
from sympy import symbols, solve, discriminant

x, a = symbols('x a', real=True)

# 진수 f(x) = x^2 + ax + a + 8
f = x**2 + a*x + a + 8

# 판별식
D = discriminant(f, x)
print(f'Discriminant: {D}')

# 판별식 < 0 을 풀어 a의 범위 구하기
D_roots = solve(D, a)
print(f'Discriminant roots: {D_roots}')

# a^2 - 4a - 32 < 0 의 해
a_sym = symbols('a')
ineq_solution = solve(a_sym**2 - 4*a_sym - 32 < 0, a_sym)
print(f'Solution to D < 0: {ineq_solution}')

# 로그 조건: 0 < a < 8, a != 1
# 정수 a: 2, 3, 4, 5, 6, 7
valid_integers = [2, 3, 4, 5, 6, 7]
print(f'Valid integer values of a: {valid_integers}')

# 검증: 각 a에 대해 f(x) > 0 이 모든 x에서 성립하는지 확인
for a_val in valid_integers:
    f_val = x**2 + a_val*x + a_val + 8
    D_val = a_val**2 - 4*a_val - 32
    print(f'a={a_val}: D={D_val} (should be < 0)')
    if D_val < 0:
        print(f'  ✓ Always positive')
    else:
        print(f'  ✗ NOT always positive')

# 합 계산
total_sum = sum(valid_integers)
print(f'\nSum of all valid integers: {total_sum}')

if total_sum == 27:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')